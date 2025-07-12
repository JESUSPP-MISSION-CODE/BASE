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
        #connection_string = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
        
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

if __name__ == "__main__":
    main()

# 사용 예시:
"""
# 1. 필요한 패키지 설치
pip install pymongo pandas python-dotenv

# 2. 환경 변수 설정 (.env 파일 생성)
MONGODB_URI=mongodb+srv://username:password@cluster-name.mongodb.net/?retryWrites=true&w=majority

# 3. 실행
python mongodb_atlas_sample.py
"""