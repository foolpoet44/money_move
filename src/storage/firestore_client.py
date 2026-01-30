"""
Firestore Client for Money Flow Prediction System
InfluxDB와 Redis를 대체하여 무료 티어 최적화
"""

from google.cloud import firestore
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from loguru import logger


class FirestoreClient:
    """Firestore 클라이언트 (InfluxDB + Redis 대체)"""
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize Firestore client
        
        Args:
            project_id: Google Cloud 프로젝트 ID (None이면 자동 감지)
        """
        self.db = firestore.Client(project=project_id)
        self.retention_days = 30  # 데이터 보관 기간 (무료 티어 최적화)
        
    # ==================== Market Data ====================
    
    def write_market_data(self, symbol: str, data: Dict[str, Any]) -> None:
        """
        시장 데이터 저장
        
        Args:
            symbol: 티커 심볼 (예: 'SPY', 'DXY')
            data: 저장할 데이터 딕셔너리
        """
        try:
            doc_ref = self.db.collection('market_data').document()
            doc_data = {
                'symbol': symbol,
                'timestamp': datetime.utcnow(),
                **data
            }
            doc_ref.set(doc_data)
            logger.debug(f"Market data saved: {symbol}")
        except Exception as e:
            logger.error(f"Failed to write market data: {e}")
    
    def read_market_data(
        self, 
        symbol: str, 
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        시장 데이터 조회
        
        Args:
            symbol: 티커 심볼
            start_time: 시작 시간 (None이면 24시간 전)
            end_time: 종료 시간 (None이면 현재)
            limit: 최대 결과 수
        
        Returns:
            DataFrame with market data
        """
        try:
            if start_time is None:
                start_time = datetime.utcnow() - timedelta(days=1)
            if end_time is None:
                end_time = datetime.utcnow()
            
            query = (
                self.db.collection('market_data')
                .where('symbol', '==', symbol)
                .where('timestamp', '>=', start_time)
                .where('timestamp', '<=', end_time)
                .order_by('timestamp', direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            
            docs = query.stream()
            data = [doc.to_dict() for doc in docs]
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df.sort_values('timestamp')
            
        except Exception as e:
            logger.error(f"Failed to read market data: {e}")
            return pd.DataFrame()
    
    # ==================== Signals ====================
    
    def create_signal(self, signal_data: Dict[str, Any]) -> str:
        """
        신호 생성
        
        Args:
            signal_data: 신호 데이터 (scenario, severity, recommendation 등)
        
        Returns:
            생성된 신호 문서 ID
        """
        try:
            doc_ref = self.db.collection('signals').document()
            doc_data = {
                'timestamp': datetime.utcnow(),
                'active': True,
                **signal_data
            }
            doc_ref.set(doc_data)
            logger.info(f"Signal created: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Failed to create signal: {e}")
            return ""
    
    def get_active_signals(
        self,
        severity: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        활성 신호 조회
        
        Args:
            severity: 심각도 필터 (INFO, WARNING, CRITICAL, EMERGENCY)
            limit: 최대 결과 수
        
        Returns:
            활성 신호 리스트
        """
        try:
            query = (
                self.db.collection('signals')
                .where('active', '==', True)
            )
            
            if severity:
                query = query.where('severity', '==', severity)
            
            query = (
                query.order_by('timestamp', direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            
            docs = query.stream()
            return [{'id': doc.id, **doc.to_dict()} for doc in docs]
            
        except Exception as e:
            logger.error(f"Failed to get active signals: {e}")
            return []
    
    def deactivate_signal(self, signal_id: str) -> bool:
        """
        신호 비활성화
        
        Args:
            signal_id: 신호 문서 ID
        
        Returns:
            성공 여부
        """
        try:
            doc_ref = self.db.collection('signals').document(signal_id)
            doc_ref.update({
                'active': False,
                'deactivated_at': datetime.utcnow()
            })
            logger.info(f"Signal deactivated: {signal_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to deactivate signal: {e}")
            return False
    
    # ==================== Predictions ====================
    
    def save_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """
        예측 결과 저장
        
        Args:
            prediction_data: 예측 데이터 (model_type, direction, confidence 등)
        
        Returns:
            생성된 예측 문서 ID
        """
        try:
            doc_ref = self.db.collection('predictions').document()
            doc_data = {
                'created_at': datetime.utcnow(),
                **prediction_data
            }
            doc_ref.set(doc_data)
            logger.debug(f"Prediction saved: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Failed to save prediction: {e}")
            return ""
    
    def get_latest_prediction(
        self,
        model_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        최신 예측 조회
        
        Args:
            model_type: 모델 타입 필터 (lstm, transformer, ensemble)
        
        Returns:
            최신 예측 데이터
        """
        try:
            query = self.db.collection('predictions')
            
            if model_type:
                query = query.where('model_type', '==', model_type)
            
            query = (
                query.order_by('created_at', direction=firestore.Query.DESCENDING)
                .limit(1)
            )
            
            docs = list(query.stream())
            if docs:
                return {'id': docs[0].id, **docs[0].to_dict()}
            return None
            
        except Exception as e:
            logger.error(f"Failed to get latest prediction: {e}")
            return None
    
    # ==================== Cache (Redis 대체) ====================
    
    def set_cache(self, key: str, value: Dict[str, Any], ttl_seconds: int = 300) -> bool:
        """
        캐시 데이터 저장 (Redis 대체)
        
        Args:
            key: 캐시 키
            value: 저장할 값
            ttl_seconds: 만료 시간 (초)
        
        Returns:
            성공 여부
        """
        try:
            doc_ref = self.db.collection('cache').document(key)
            doc_data = {
                'value': value,
                'expires_at': datetime.utcnow() + timedelta(seconds=ttl_seconds),
                'created_at': datetime.utcnow()
            }
            doc_ref.set(doc_data)
            return True
        except Exception as e:
            logger.error(f"Failed to set cache: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """
        캐시 데이터 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            캐시된 값 (만료되었거나 없으면 None)
        """
        try:
            doc_ref = self.db.collection('cache').document(key)
            doc = doc_ref.get()
            
            if not doc.exists:
                return None
            
            data = doc.to_dict()
            
            # 만료 확인
            if data['expires_at'] < datetime.utcnow():
                # 만료된 캐시 삭제
                doc_ref.delete()
                return None
            
            return data['value']
            
        except Exception as e:
            logger.error(f"Failed to get cache: {e}")
            return None
    
    # ==================== Analytics ====================
    
    def save_analytics(self, metric_name: str, value: float, metadata: Optional[Dict] = None) -> None:
        """
        분석 메트릭 저장
        
        Args:
            metric_name: 메트릭 이름 (예: 'risk_score', 'correlation')
            value: 메트릭 값
            metadata: 추가 메타데이터
        """
        try:
            doc_ref = self.db.collection('analytics').document()
            doc_data = {
                'metric_name': metric_name,
                'value': value,
                'timestamp': datetime.utcnow(),
                'metadata': metadata or {}
            }
            doc_ref.set(doc_data)
        except Exception as e:
            logger.error(f"Failed to save analytics: {e}")
    
    # ==================== Data Cleanup ====================
    
    def cleanup_old_data(self) -> Dict[str, int]:
        """
        오래된 데이터 정리 (무료 티어 최적화)
        
        Returns:
            삭제된 문서 수 (컬렉션별)
        """
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        deleted_counts = {}
        
        collections_to_clean = ['market_data', 'signals', 'predictions', 'analytics', 'cache']
        
        for collection_name in collections_to_clean:
            try:
                query = (
                    self.db.collection(collection_name)
                    .where('timestamp', '<', cutoff_date)
                    .limit(500)  # 배치 크기
                )
                
                docs = list(query.stream())
                deleted = 0
                
                for doc in docs:
                    doc.reference.delete()
                    deleted += 1
                
                deleted_counts[collection_name] = deleted
                
                if deleted > 0:
                    logger.info(f"Cleaned {deleted} old documents from {collection_name}")
                    
            except Exception as e:
                logger.error(f"Failed to cleanup {collection_name}: {e}")
                deleted_counts[collection_name] = 0
        
        return deleted_counts


# Singleton instance
_firestore_client = None


def get_firestore_client(project_id: Optional[str] = None) -> FirestoreClient:
    """
    Get singleton Firestore client instance
    
    Args:
        project_id: Google Cloud 프로젝트 ID
    
    Returns:
        FirestoreClient instance
    """
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = FirestoreClient(project_id)
    return _firestore_client
