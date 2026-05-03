import { useEffect, useCallback, useRef } from 'react';
import { useInvestigationStore, Claim } from '@/store/useInvestigationStore';

export const useWebSocket = (jobId: string | null) => {
  const { 
    setStatus, 
    setGlobalScore, 
    setClaims, 
    upsertClaim,
    setProgress,
    setAuditLogs
  } = useInvestigationStore();
  
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (!jobId) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:8000/ws/${jobId}`;
    
    console.log(`Connecting to WebSocket: ${wsUrl}`);
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      console.log('WebSocket Connected');
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('WS Message:', message);

      switch (message.type) {
        case 'status':
          setStatus(message.data);
          break;
        case 'progress':
          setProgress(message.data);
          break;
        case 'claims_extracted':
          const claimMap: Record<string, Claim> = {};
          message.data.forEach((c: Claim) => {
            claimMap[c.id] = c;
          });
          setClaims(claimMap);
          break;
        case 'state_update':
          const { global_score, red_flag_count, claims, audit_logs } = message.data;
          setGlobalScore(global_score, red_flag_count);
          setClaims(claims);
          if (audit_logs) {
            setAuditLogs(audit_logs);
          }
          break;
        case 'error':
          console.error('Investigation Error:', message.data);
          setStatus('failed');
          break;
      }
    };

    socket.onclose = () => {
      console.log('WebSocket Disconnected');
    };

    socketRef.current = socket;
  }, [jobId, setStatus, setGlobalScore, setClaims, setProgress, setAuditLogs]);

  useEffect(() => {
    connect();
    return () => {
      socketRef.current?.close();
    };
  }, [connect]);

  return socketRef.current;
};
