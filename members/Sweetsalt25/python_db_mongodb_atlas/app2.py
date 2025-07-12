import pymongo
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 환경 변수 로드 (선택사항)
load_dotenv()

def connect_to_mongodb():
    """MongoDB Atlas에 연결"""
    try:
        # MongoDB Atlas 연결 문자열
        # 실제 사용시에는 username, password, cluster 정보를 변경해야 합니다
        # connection_string = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
        
        # 환경 변수에서 연결 문자열 가져오기 (권장)
        connection_string = os.getenv('MONGODB_URI')
        
        client = MongoClient(connection_string)
        
        # 연결 테스트
        client.admin.command('ping')
        print("MongoDB Atlas 연결 성공!")
        
        return client
    
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
        return None

def get_database_collections(client, database_name):
    """데이터베이스의 컬렉션 목록 조회"""
    try:
        db = client[database_name]
        collections = db.list_collection_names()
        return collections
    except Exception as e:
        print(f"컬렉션 조회 실패: {e}")
        return []

def display_collection_as_table(client, database_name, collection_name, limit=10):
    """컬렉션 데이터를 테이블 형태로 출력"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        # 문서 수 조회
        total_count = collection.count_documents({})
        print(f"\n=== {collection_name} 컬렉션 ===")
        print(f"총 문서 수: {total_count}")
        
        # 데이터 조회 (limit 적용)
        cursor = collection.find().limit(limit)
        documents = list(cursor)
        
        if not documents:
            print("데이터가 없습니다.")
            return
        
        # pandas DataFrame으로 변환하여 테이블 형태로 출력
        df = pd.DataFrame(documents)
        
        # _id 컬럼을 문자열로 변환 (보기 편하게)
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        
        print(f"\n상위 {limit}개 데이터:")
        print(df.to_string(index=False))
        
        return df
        
    except Exception as e:
        print(f"데이터 조회 실패: {e}")
        return None

def main():
    """메인 함수"""
    # MongoDB Atlas 연결
    client = connect_to_mongodb()
    
    if client is None:
        return
    
    try:
        # 데이터베이스 목록 조회
        databases = client.list_database_names()
        print("\n사용 가능한 데이터베이스:")
        for db in databases:
            print(f"- {db}")
        
        # 예시: 특정 데이터베이스 사용
        database_name = "sample_mflix"  # 실제 데이터베이스 이름으로 변경
        
        # 컬렉션 목록 조회
        collections = get_database_collections(client, database_name)
        print(f"\n'{database_name}' 데이터베이스의 컬렉션:")
        for col in collections:
            print(f"- {col}")
        
        # 예시: 특정 컬렉션 데이터 테이블로 출력
        if collections:
            collection_name = collections[0]  # 첫 번째 컬렉션 사용
            df = display_collection_as_table(client, database_name, collection_name, limit=5)
            
            if df is not None:
                print(f"\n컬럼 정보:")
                print(df.dtypes)
    
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
    
    finally:
        # 연결 종료
        if client:
            client.close()
            print("\nMongoDB 연결이 종료되었습니다.")

# 추가 유틸리티 함수들
def search_documents(client, database_name, collection_name, query, limit=10):
    """특정 조건으로 문서 검색"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        cursor = collection.find(query).limit(limit)
        documents = list(cursor)
        
        if documents:
            df = pd.DataFrame(documents)
            if '_id' in df.columns:
                df['_id'] = df['_id'].astype(str)
            return df
        else:
            print("검색 결과가 없습니다.")
            return None
            
    except Exception as e:
        print(f"검색 실패: {e}")
        return None

def get_collection_stats(client, database_name, collection_name):
    """컬렉션 통계 정보 조회"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        # 기본 통계
        stats = db.command("collStats", collection_name)
        
        print(f"\n=== {collection_name} 컬렉션 통계 ===")
        print(f"문서 수: {stats.get('count', 0):,}")
        print(f"평균 문서 크기: {stats.get('avgObjSize', 0):,.2f} bytes")
        print(f"총 크기: {stats.get('size', 0):,} bytes")
        print(f"인덱스 수: {stats.get('nindexes', 0)}")
        
    except Exception as e:
        print(f"통계 조회 실패: {e}")

# 인터랙티브 관리 기능들
def create_database_and_collection(client, database_name, collection_name):
    """새 데이터베이스와 컬렉션 생성"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        # 빈 문서를 삽입해서 컬렉션 생성 (MongoDB는 데이터가 있어야 실제 생성됨)
        temp_doc = {"_temp": "temp_document_for_creation"}
        collection.insert_one(temp_doc)
        
        # 임시 문서 삭제
        collection.delete_one({"_temp": "temp_document_for_creation"})
        
        print(f"데이터베이스 '{database_name}'와 컬렉션 '{collection_name}'이 생성되었습니다.")
        return True
        
    except Exception as e:
        print(f"데이터베이스/컬렉션 생성 실패: {e}")
        return False

def delete_collection(client, database_name, collection_name):
    """컬렉션 삭제"""
    try:
        db = client[database_name]
        
        # 컬렉션 존재 확인
        if collection_name not in db.list_collection_names():
            print(f"컬렉션 '{collection_name}'이 존재하지 않습니다.")
            return False
        
        db.drop_collection(collection_name)
        print(f"컬렉션 '{collection_name}'이 삭제되었습니다.")
        return True
        
    except Exception as e:
        print(f"컬렉션 삭제 실패: {e}")
        return False

def insert_document(client, database_name, collection_name, document):
    """문서 삽입"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        result = collection.insert_one(document)
        print(f"문서가 삽입되었습니다. ID: {result.inserted_id}")
        return result.inserted_id
        
    except Exception as e:
        print(f"문서 삽입 실패: {e}")
        return None

def insert_multiple_documents(client, database_name, collection_name, documents):
    """여러 문서 삽입"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        result = collection.insert_many(documents)
        print(f"{len(result.inserted_ids)}개의 문서가 삽입되었습니다.")
        return result.inserted_ids
        
    except Exception as e:
        print(f"문서 삽입 실패: {e}")
        return None

def delete_document(client, database_name, collection_name, query):
    """문서 삭제"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        result = collection.delete_one(query)
        if result.deleted_count > 0:
            print(f"문서가 삭제되었습니다. 삭제된 문서 수: {result.deleted_count}")
        else:
            print("삭제할 문서를 찾을 수 없습니다.")
        
        return result.deleted_count
        
    except Exception as e:
        print(f"문서 삭제 실패: {e}")
        return 0

def update_document(client, database_name, collection_name, query, update_data):
    """문서 업데이트"""
    try:
        db = client[database_name]
        collection = db[collection_name]
        
        result = collection.update_one(query, {"$set": update_data})
        if result.modified_count > 0:
            print(f"문서가 업데이트되었습니다. 수정된 문서 수: {result.modified_count}")
        else:
            print("업데이트할 문서를 찾을 수 없습니다.")
        
        return result.modified_count
        
    except Exception as e:
        print(f"문서 업데이트 실패: {e}")
        return 0

def interactive_menu():
    """인터랙티브 메뉴"""
    client = connect_to_mongodb()
    if client is None:
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("MongoDB Atlas 인터랙티브 관리 도구")
            print("="*50)
            print("1. 데이터베이스 목록 조회")
            print("2. 컬렉션 목록 조회")
            print("3. 데이터베이스/컬렉션 생성")
            print("4. 컬렉션 삭제")
            print("5. 문서 삽입")
            print("6. 여러 문서 삽입")
            print("7. 문서 검색")
            print("8. 문서 업데이트")
            print("9. 문서 삭제")
            print("10. 컬렉션 데이터 테이블로 보기")
            print("11. 컬렉션 통계")
            print("0. 종료")
            print("="*50)
            
            choice = input("선택하세요: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                show_databases(client)
            elif choice == "2":
                show_collections(client)
            elif choice == "3":
                create_db_collection_interactive(client)
            elif choice == "4":
                delete_collection_interactive(client)
            elif choice == "5":
                insert_document_interactive(client)
            elif choice == "6":
                insert_multiple_documents_interactive(client)
            elif choice == "7":
                search_documents_interactive(client)
            elif choice == "8":
                update_document_interactive(client)
            elif choice == "9":
                delete_document_interactive(client)
            elif choice == "10":
                show_collection_table_interactive(client)
            elif choice == "11":
                show_collection_stats_interactive(client)
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.")
                
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if client:
            client.close()
            print("MongoDB 연결이 종료되었습니다.")

def show_databases(client):
    """데이터베이스 목록 표시"""
    try:
        databases = client.list_database_names()
        print("\n=== 데이터베이스 목록 ===")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")
    except Exception as e:
        print(f"데이터베이스 목록 조회 실패: {e}")

def show_collections(client):
    """컬렉션 목록 표시"""
    try:
        databases = client.list_database_names()
        print("\n사용 가능한 데이터베이스:")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")
        
        db_choice = input("데이터베이스 번호를 선택하세요: ").strip()
        try:
            db_index = int(db_choice) - 1
            if 0 <= db_index < len(databases):
                db_name = databases[db_index]
                collections = get_database_collections(client, db_name)
                print(f"\n=== '{db_name}' 데이터베이스의 컬렉션 목록 ===")
                for i, col in enumerate(collections, 1):
                    print(f"{i}. {col}")
            else:
                print("잘못된 번호입니다.")
        except ValueError:
            print("숫자를 입력해주세요.")
    except Exception as e:
        print(f"컬렉션 목록 조회 실패: {e}")

def create_db_collection_interactive(client):
    """대화형 DB/컬렉션 생성"""
    try:
        db_name = input("생성할 데이터베이스 이름: ").strip()
        col_name = input("생성할 컬렉션 이름: ").strip()
        
        if db_name and col_name:
            create_database_and_collection(client, db_name, col_name)
        else:
            print("데이터베이스와 컬렉션 이름을 모두 입력해주세요.")
    except Exception as e:
        print(f"생성 중 오류 발생: {e}")

def delete_collection_interactive(client):
    """대화형 컬렉션 삭제"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("삭제할 컬렉션 이름: ").strip()
        
        if db_name and col_name:
            confirm = input(f"정말로 '{col_name}' 컬렉션을 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_collection(client, db_name, col_name)
            else:
                print("삭제가 취소되었습니다.")
        else:
            print("데이터베이스와 컬렉션 이름을 모두 입력해주세요.")
    except Exception as e:
        print(f"삭제 중 오류 발생: {e}")

def insert_document_interactive(client):
    """대화형 문서 삽입"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        print("\n문서 데이터를 입력하세요 (JSON 형태):")
        print("예: {\"name\": \"홍길동\", \"age\": 30, \"city\": \"서울\"}")
        doc_str = input("문서 데이터: ").strip()
        
        try:
            import json
            document = json.loads(doc_str)
            insert_document(client, db_name, col_name, document)
        except json.JSONDecodeError:
            print("올바른 JSON 형태로 입력해주세요.")
    except Exception as e:
        print(f"문서 삽입 중 오류 발생: {e}")

def insert_multiple_documents_interactive(client):
    """대화형 여러 문서 삽입"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        print("\n샘플 데이터를 삽입하시겠습니까? (y/n)")
        use_sample = input("선택: ").strip().lower()
        
        if use_sample == 'y':
            sample_docs = [
                {"name": "홍길동", "age": 30, "city": "서울", "job": "개발자"},
                {"name": "김철수", "age": 25, "city": "부산", "job": "디자이너"},
                {"name": "이영희", "age": 28, "city": "대구", "job": "마케터"},
                {"name": "박민수", "age": 32, "city": "인천", "job": "기획자"},
                {"name": "최지영", "age": 27, "city": "광주", "job": "분석가"}
            ]
            insert_multiple_documents(client, db_name, col_name, sample_docs)
        else:
            print("JSON 배열 형태로 입력하세요:")
            print("예: [{\"name\": \"홍길동\", \"age\": 30}, {\"name\": \"김철수\", \"age\": 25}]")
            docs_str = input("문서 배열: ").strip()
            
            try:
                import json
                documents = json.loads(docs_str)
                if isinstance(documents, list):
                    insert_multiple_documents(client, db_name, col_name, documents)
                else:
                    print("배열 형태로 입력해주세요.")
            except json.JSONDecodeError:
                print("올바른 JSON 배열 형태로 입력해주세요.")
    except Exception as e:
        print(f"문서 삽입 중 오류 발생: {e}")

def search_documents_interactive(client):
    """대화형 문서 검색"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        print("\n검색 조건을 입력하세요:")
        print("1. 모든 문서 검색 (빈 문자열 입력)")
        print("2. 조건 검색 (예: {\"age\": 30} 또는 {\"city\": \"서울\"})")
        query_str = input("검색 조건: ").strip()
        
        try:
            import json
            if query_str == "":
                query = {}
            else:
                query = json.loads(query_str)
            
            limit = input("최대 결과 수 (기본값: 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            
            df = search_documents(client, db_name, col_name, query, limit)
            if df is not None:
                print(f"\n검색 결과 ({len(df)}개):")
                print(df.to_string(index=False))
        except json.JSONDecodeError:
            print("올바른 JSON 형태로 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
    except Exception as e:
        print(f"검색 중 오류 발생: {e}")

def update_document_interactive(client):
    """대화형 문서 업데이트"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        print("\n업데이트할 문서의 조건을 입력하세요:")
        print("예: {\"name\": \"홍길동\"}")
        query_str = input("검색 조건: ").strip()
        
        print("\n업데이트할 데이터를 입력하세요:")
        print("예: {\"age\": 31, \"city\": \"부산\"}")
        update_str = input("업데이트 데이터: ").strip()
        
        try:
            import json
            query = json.loads(query_str)
            update_data = json.loads(update_str)
            
            update_document(client, db_name, col_name, query, update_data)
        except json.JSONDecodeError:
            print("올바른 JSON 형태로 입력해주세요.")
    except Exception as e:
        print(f"업데이트 중 오류 발생: {e}")

def delete_document_interactive(client):
    """대화형 문서 삭제"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        print("\n삭제할 문서의 조건을 입력하세요:")
        print("예: {\"name\": \"홍길동\"}")
        query_str = input("검색 조건: ").strip()
        
        try:
            import json
            query = json.loads(query_str)
            
            confirm = input(f"정말로 조건 '{query_str}'에 맞는 문서를 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_document(client, db_name, col_name, query)
            else:
                print("삭제가 취소되었습니다.")
        except json.JSONDecodeError:
            print("올바른 JSON 형태로 입력해주세요.")
    except Exception as e:
        print(f"삭제 중 오류 발생: {e}")

def show_collection_table_interactive(client):
    """대화형 컬렉션 테이블 보기"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        limit = input("최대 표시 수 (기본값: 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        
        display_collection_as_table(client, db_name, col_name, limit)
    except ValueError:
        print("숫자를 입력해주세요.")
    except Exception as e:
        print(f"테이블 표시 중 오류 발생: {e}")

def show_collection_stats_interactive(client):
    """대화형 컬렉션 통계 보기"""
    try:
        db_name = input("데이터베이스 이름: ").strip()
        col_name = input("컬렉션 이름: ").strip()
        
        get_collection_stats(client, db_name, col_name)
    except Exception as e:
        print(f"통계 조회 중 오류 발생: {e}")

if __name__ == "__main__":
    print("MongoDB Atlas 관리 도구")
    print("1. 기본 실행")
    print("2. 인터랙티브 메뉴")
    
    choice = input("선택하세요 (1 또는 2): ").strip()
    
    if choice == "2":
        interactive_menu()
    else:
        main()

# 사용 예시:
"""
# 1. 필요한 패키지 설치
pip install pymongo pandas python-dotenv

# 2. 환경 변수 설정 (.env 파일 생성)
MONGODB_URI=mongodb+srv://username:password@cluster-name.mongodb.net/?retryWrites=true&w=majority

# 3. 실행
python mongodb_atlas_sample.py

# 4. 인터랙티브 메뉴 선택 후 다양한 기능 사용:
# - 데이터베이스/컬렉션 생성
# - 문서 삽입/삭제/업데이트
# - 검색 및 테이블 형태 출력
# - 통계 정보 확인
"""