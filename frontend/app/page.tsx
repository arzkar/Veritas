"use client";

import React, { useState, useEffect, useCallback } from 'react';
import { useInvestigationStore, Claim, Evidence } from '@/store/useInvestigationStore';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { ModeToggle } from '@/components/mode-toggle';
import { 
  ShieldAlert, 
  Search, 
  FileText, 
  Activity, 
  AlertTriangle,
  CheckCircle2,
  Clock,
  Upload,
  Loader2,
  ChevronRight,
  Database,
  Terminal,
  Zap,
  ChevronLeft,
  LayoutGrid,
  BarChart3,
  Network,
  Trash2,
  ArrowRight
} from 'lucide-react';

export default function Dashboard() {
  const { 
    currentJobId,
    companyName, 
    globalCredibilityScore, 
    claims, 
    status,
    redFlagCount,
    jobs,
    auditLogs,
    progress,
    setJob,
    setStatus,
    setJobs,
    loadJobData,
    reset,
    evidence
  } = useInvestigationStore();

  const [uploading, setUploading] = useState(false);
  const [selectedClaimId, setSelectedClaimId] = useState<string | null>(null);

  // Connect to live investigation updates
  useWebSocket(currentJobId);

  const fetchJobs = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8000/jobs');
      const data = await response.json();
      setJobs(data);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    }
  }, [setJobs]);

  // Fetch jobs on mount
  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 10000); 
    return () => clearInterval(interval);
  }, [fetchJobs]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setStatus('ingesting');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('company_name', file.name.replace('.pdf', ''));

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setJob(data.job_id, file.name.replace('.pdf', ''));
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteJob = async (e: React.MouseEvent, jobId: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this investigation?')) return;

    try {
      await fetch(`http://localhost:8000/jobs/${jobId}`, { method: 'DELETE' });
      fetchJobs();
      if (currentJobId === jobId) reset();
    } catch (error) {
      console.error('Delete failed:', error);
    }
  };

  const claimList = Object.values(claims);
  const selectedClaim = selectedClaimId ? claims[selectedClaimId] : null;
  const claimEvidence = selectedClaimId ? (evidence[selectedClaimId] || []) : [];

  // --- Layer 1: Project Repository View ---
  if (!currentJobId) {
    return (
      <div className="flex flex-col h-screen bg-background text-foreground font-sans">
        <header className="h-16 border-b border-border px-8 flex items-center justify-between bg-card/20 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-primary rounded-sm flex items-center justify-center font-bold italic text-primary-foreground text-xl shadow-lg dark:shadow-primary/5">V</div>
            <div>
               <h1 className="text-sm font-mono font-bold tracking-[0.3em] text-foreground">VERITAS</h1>
               <p className="text-[10px] text-muted-foreground font-mono tracking-tighter uppercase">Investigative Intelligence Terminal</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ModeToggle />
            <Separator orientation="vertical" className="h-6" />
            <input type="file" id="main-upload" className="hidden" accept=".pdf" onChange={handleFileUpload} />
            <Button 
              className="h-10 px-6 font-bold font-mono text-[11px] rounded-sm transition-all shadow-sm"
              onClick={() => document.getElementById('main-upload')?.click()}
              disabled={uploading}
            >
              {uploading ? <Loader2 className="w-3.5 h-3.5 mr-2 animate-spin" /> : <Upload className="w-3.5 h-3.5 mr-2" />}
              INITIALIZE NEW DECK
            </Button>
          </div>
        </header>

        <main className="flex-1 p-12 overflow-y-auto bg-[radial-gradient(circle_at_50%_0%,rgba(var(--primary-rgb),0.05),transparent)]">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-10">
               <div className="flex items-center gap-2 text-muted-foreground">
                  <LayoutGrid className="w-4 h-4" />
                  <h2 className="text-xs font-bold uppercase tracking-[0.2em] font-mono">Diligence Repository</h2>
               </div>
               <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">{jobs.length} Investigations Cached</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
              {jobs.length === 0 ? (
                <div className="col-span-full h-80 border border-dashed border-border bg-card/10 rounded-sm flex flex-col items-center justify-center text-muted-foreground">
                  <div className="w-16 h-16 rounded-full bg-card/50 flex items-center justify-center mb-6 border border-border">
                    <Database className="w-6 h-6 opacity-30" />
                  </div>
                  <p className="font-mono text-xs uppercase tracking-[0.3em]">No Active Investigations</p>
                  <p className="text-[11px] mt-2 opacity-50">Upload source material to begin forensic analysis.</p>
                </div>
              ) : (
                jobs.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).map((job) => (
                  <Card 
                    key={job.job_id} 
                    className="bg-card border-border hover:border-primary/50 cursor-pointer transition-all group rounded-none relative overflow-hidden"
                    onClick={() => loadJobData(job.job_id)}
                  >
                    <div className="absolute top-0 right-0 p-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                       <Button 
                         variant="ghost" 
                         size="icon" 
                         className="h-7 w-7 text-destructive hover:bg-destructive/10 hover:text-destructive"
                         onClick={(e) => handleDeleteJob(e, job.job_id)}
                       >
                         <Trash2 className="w-3.5 h-3.5" />
                       </Button>
                       <div className="h-7 w-7 flex items-center justify-center text-muted-foreground">
                          <ChevronRight className="w-4 h-4" />
                       </div>
                    </div>
                    <CardContent className="p-8">
                      <div className="flex justify-between items-start mb-10">
                        <div className="w-10 h-10 bg-background border border-border flex items-center justify-center group-hover:border-primary transition-colors">
                          <FileText className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                        </div>
                        <Badge variant="outline" className={`font-mono text-[9px] tracking-tight uppercase rounded-none border-border text-muted-foreground ${
                          job.status === 'completed' ? 'border-emerald-500/30 text-emerald-500 bg-emerald-500/5' : ''
                        }`}>
                          {job.status}
                        </Badge>
                      </div>
                      <h3 className="text-sm font-bold uppercase tracking-widest mb-1 text-foreground font-mono truncate">{job.company}</h3>
                      <p className="text-[10px] text-muted-foreground font-mono mb-4">{new Date(job.created_at).toLocaleString()}</p>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </div>
        </main>
      </div>
    );
  }

  // --- Layer 2: Investigative Terminal View ---
  return (
    <div className="flex flex-col h-screen max-h-screen overflow-hidden bg-background text-foreground font-sans">
      {/* Top Bar */}
      <header className="h-14 border-b border-border px-4 flex items-center justify-between bg-card/20 backdrop-blur-md z-50">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={reset} className="h-8 px-3 hover:bg-accent text-muted-foreground font-mono text-[10px] tracking-widest rounded-none">
            <ChevronLeft className="w-3.5 h-3.5 mr-1" /> EXIT
          </Button>
          <Separator orientation="vertical" className="h-6" />
          <div className="flex items-center gap-3 ml-2">
            <div className="w-6 h-6 bg-primary rounded-sm flex items-center justify-center text-[11px] font-bold italic text-primary-foreground shadow-sm">V</div>
            <div>
              <h1 className="text-[11px] font-mono font-bold tracking-[0.2em] text-foreground uppercase">{companyName}</h1>
              <p className="text-[9px] text-muted-foreground uppercase font-mono tracking-tighter">NODE_ID: {currentJobId.split('-')[0]}</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <ModeToggle />
        </div>
      </header>

      {/* Main Investigative Surface */}
      <main className="flex-1 flex overflow-hidden">
        
        {/* Left Panel: Claims */}
        <section className="w-80 border-r border-border bg-card/10 flex flex-col">
          <div className="p-4 border-b border-border bg-card/30 flex items-center justify-between">
            <h2 className="text-[10px] font-bold uppercase tracking-[0.3em] text-muted-foreground flex items-center gap-2">
              <Activity className="w-3.5 h-3.5" /> Primitives
            </h2>
            <span className="text-[10px] font-mono text-muted-foreground">{claimList.length}</span>
          </div>
          <ScrollArea className="flex-1">
            <div className="p-3 space-y-3">
              {claimList.length === 0 ? (
                <div className="h-64 flex flex-col items-center justify-center opacity-20 text-muted-foreground">
                  <BarChart3 className="w-8 h-8 mb-4 stroke-[1px]" />
                  <span className="text-[9px] uppercase font-mono tracking-[0.2em]">Decomposing Deck...</span>
                </div>
              ) : (
                claimList.sort((a, b) => b.importance - a.importance).map((claim) => (
                  <div 
                    key={claim.id} 
                    onClick={() => setSelectedClaimId(claim.id)}
                    className={`p-4 rounded-none border border-border bg-card/40 hover:bg-card/60 transition-all cursor-pointer border-l-2 relative group ${
                      selectedClaimId === claim.id ? 'ring-1 ring-primary/50' : ''
                    } ${
                      claim.belief === 'contradicted' ? 'border-l-destructive shadow-[inset_0_0_20px_rgba(239,68,68,0.02)]' : 
                      claim.belief === 'supported' ? 'border-l-emerald-500/80' : 
                      'border-l-muted'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-2.5">
                      <span className="text-[8px] font-mono text-muted-foreground tracking-tighter uppercase px-1.5 py-0.5 border border-border">Slide {claim.primary_slide.toString().padStart(2, '0')}</span>
                      <EpistemicBadge status={claim.belief} />
                    </div>
                    <p className="text-[11px] font-medium leading-[1.6] text-foreground">
                      {claim.statement}
                    </p>
                    <div className="mt-4 flex items-center justify-between text-[9px] font-mono text-muted-foreground uppercase tracking-tighter border-t border-border pt-3">
                      <span className="truncate max-w-[120px]">{claim.category}</span>
                      <span className="flex items-center gap-1.5">
                        <Zap className="w-2.5 h-2.5" />
                        IMP <span className={claim.importance > 0.8 ? 'text-foreground font-bold' : ''}>{claim.importance.toFixed(1)}</span>
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </section>

        {/* Center: Audit Log (The Glass Box) */}
        <section className="flex-1 bg-background flex flex-col border-r border-border">
          {/* Real-time Metrics Bar */}
          <div className="p-4 border-b border-border bg-card/20 grid grid-cols-3 gap-6">
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                 <span className="text-[9px] text-muted-foreground uppercase font-mono tracking-widest">Global Credibility</span>
                 <span className={`text-[11px] font-mono font-bold ${globalCredibilityScore < 0.5 ? 'text-destructive' : 'text-emerald-500'}`}>
                    {(globalCredibilityScore * 100).toFixed(0)}%
                 </span>
              </div>
              <Progress value={globalCredibilityScore * 100} className="h-1 bg-card rounded-none" />
            </div>

            <div className="flex flex-col justify-center border-l border-border pl-6">
               <span className="text-[9px] text-muted-foreground uppercase font-mono tracking-widest">Red Flags</span>
               <span className={`text-lg font-mono font-bold leading-none ${redFlagCount > 0 ? 'text-destructive' : 'text-muted-foreground/30'}`}>
                  {redFlagCount.toString().padStart(2, '0')}
               </span>
            </div>

            <div className="flex flex-col justify-center border-l border-border pl-6">
               <span className="text-[9px] text-muted-foreground uppercase font-mono tracking-widest">System Status</span>
               <div className="flex items-center gap-2 mt-1">
                  <div className={`w-1.5 h-1.5 rounded-full ${status === 'investigating' ? 'bg-amber-500 animate-pulse' : status === 'ingesting' ? 'bg-blue-500 animate-pulse' : 'bg-green-500'}`} />
                  <span className="text-[10px] font-mono uppercase text-foreground/80">{status}</span>
               </div>
            </div>
          </div>

          <div className="p-3 border-b border-border bg-card/10 flex items-center justify-between">
            <h2 className="text-[10px] font-bold uppercase tracking-[0.3em] text-muted-foreground flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5" /> Investigative Audit Log
            </h2>
            {status === 'ingesting' && progress && (
              <div className="flex items-center gap-3 bg-blue-500/10 border border-blue-500/20 px-3 py-1">
                 <span className="text-[9px] font-mono text-blue-400 uppercase tracking-widest">Extraction Progress</span>
                 <div className="w-32 h-1 bg-blue-900 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-400 transition-all duration-500" style={{ width: `${(progress.current / progress.total) * 100}%` }} />
                 </div>
                 <span className="text-[9px] font-mono text-blue-400">{progress.current}/{progress.total}</span>
              </div>
            )}
          </div>
          
          <ScrollArea className="flex-1">
            <div className="p-6 space-y-4 font-mono text-[11px]">
              {auditLogs.length === 0 && status !== 'ingesting' ? (
                <div className="h-96 flex flex-col items-center justify-center opacity-10 text-muted-foreground">
                  <Terminal className="w-16 h-16 mb-6 stroke-[1px]" />
                  <p className="uppercase tracking-[0.4em] text-xs">Waiting for Agent Handshake</p>
                </div>
              ) : (
                auditLogs.map((log) => (
                  <div key={log.id} className="group animate-in fade-in slide-in-from-left-4 duration-500 border-l border-border pl-4 ml-2">
                    <div className="flex items-start gap-4">
                      <span className="text-muted-foreground/60 shrink-0 text-[10px] font-mono tabular-nums">{new Date(log.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
                      <div className="flex flex-col gap-1.5">
                        <div className="flex items-center gap-3">
                          <span className={`font-bold uppercase px-2 py-0.5 rounded-none text-[9px] border font-mono tracking-tighter ${
                            log.agent_name === 'Skeptic' ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800' :
                            log.agent_name === 'Analyst' ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800' :
                            log.agent_name === 'Researcher' ? 'bg-amber-500/10 text-amber-600 dark:text-amber-500 border-amber-200 dark:border-amber-800' :
                            'bg-muted text-muted-foreground border-border'
                          }`}>
                            {log.agent_name}
                          </span>
                          <span className={`text-[11px] leading-tight ${
                            log.event_type === 'contradiction' ? 'text-destructive font-bold' :
                            log.event_type === 'skepticism' ? 'text-amber-500' :
                            log.event_type === 'completion' ? 'text-emerald-600 dark:text-emerald-500' :
                            'text-foreground/80'
                          }`}>
                            {log.message}
                          </span>
                        </div>
                        {log.metadata?.summary && (
                          <div className="ml-1 pl-4 border-l border-border mt-1 pb-2">
                             <p className="text-[10px] text-muted-foreground italic leading-relaxed max-w-3xl">{log.metadata.summary}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </section>

        {/* Right Panel: Insight Panel */}
        <section className="w-80 bg-card/10 flex flex-col">
          <Tabs defaultValue="evidence" className="flex flex-col h-full">
            <div className="px-4 border-b border-border bg-card/30">
              <TabsList className="h-12 bg-transparent w-full justify-start gap-6">
                <TabsTrigger value="evidence" className="text-[10px] font-mono uppercase tracking-[0.2em] h-full rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-foreground text-muted-foreground transition-all">
                  Evidence
                </TabsTrigger>
                <TabsTrigger value="intelligence" className="text-[10px] font-mono uppercase tracking-[0.2em] h-full rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-foreground text-muted-foreground transition-all">
                  Context
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="evidence" className="flex-1 m-0 overflow-hidden">
              <ScrollArea className="h-full p-6">
                <div className="space-y-4">
                  {selectedClaimId ? (
                    claimEvidence.length === 0 ? (
                      <div className="p-8 border border-border bg-card/20 text-center rounded-none opacity-50">
                        <Search className="w-6 h-6 text-muted-foreground/30 mx-auto mb-4 stroke-[1px]" />
                        <p className="text-[10px] text-muted-foreground uppercase font-mono tracking-[0.1em]">Research in progress...</p>
                      </div>
                    ) : (
                      claimEvidence.map((ev) => (
                        <div key={ev.id} className="p-4 border border-border bg-card/30 space-y-2 hover:bg-card/50 transition-colors">
                           <div className="flex justify-between items-start">
                              <Badge variant="outline" className="text-[8px] font-mono px-1 rounded-none opacity-60 uppercase">{ev.source_type}</Badge>
                              <span className="text-[9px] font-mono text-emerald-500">{(ev.source_authority * 100).toFixed(0)}% AUTH</span>
                           </div>
                           <h4 className="text-[11px] font-bold text-foreground leading-tight line-clamp-2">{ev.title}</h4>
                           <p className="text-[10px] text-muted-foreground leading-relaxed italic line-clamp-3">"{ev.content_snippet}"</p>
                           <a href={ev.url} target="_blank" className="flex items-center gap-1 text-[9px] text-primary hover:underline font-mono pt-1">
                             GO_TO_SOURCE <ArrowRight className="w-2.5 h-2.5" />
                           </a>
                        </div>
                      ))
                    )
                  ) : (
                   <div className="p-8 border border-border bg-card/20 text-center rounded-none">
                      <Network className="w-6 h-6 text-muted-foreground/30 mx-auto mb-4 stroke-[1px]" />
                      <p className="text-[10px] text-muted-foreground uppercase font-mono tracking-[0.2em] leading-loose">
                        Select investigative primitive to display ground-truth evidence
                      </p>
                   </div>
                  )}
                </div>
              </ScrollArea>
            </TabsContent>

            <TabsContent value="intelligence" className="flex-1 m-0 overflow-hidden">
               <div className="p-6 flex flex-col h-full space-y-6 font-mono text-foreground">
                  <div className="p-5 rounded-none border border-border bg-card/40 space-y-4 shadow-sm">
                     <h3 className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.3em] flex items-center gap-2">
                        <Activity className="w-3 h-3 text-muted-foreground/50" /> Sector Context
                     </h3>
                     <div className="space-y-4 pt-2">
                        <div className="flex justify-between items-center">
                            <span className="text-[9px] text-muted-foreground uppercase">Visibility Expectation</span>
                            <span className="text-[10px] text-emerald-500 font-bold uppercase">Optimal</span>
                        </div>
                        <div className="h-1 bg-muted overflow-hidden rounded-none">
                            <div className="h-full bg-emerald-500/50 w-[92%]" />
                        </div>
                        <div className="flex justify-between items-center pt-2">
                            <span className="text-[9px] text-muted-foreground uppercase">Audit Rigor</span>
                            <span className="text-[10px] text-foreground font-bold uppercase tracking-tighter">Aggressive</span>
                        </div>
                     </div>
                  </div>
               </div>
            </TabsContent>
          </Tabs>
        </section>

      </main>
    </div>
  );
}

function EpistemicBadge({ status }: { status: string }) {
  const configs: Record<string, { label: string, color: string, icon: any }> = {
    unverified: { label: 'UNV', color: 'text-muted-foreground border-border', icon: Clock },
    supported: { label: 'SUP', color: 'text-emerald-600 dark:text-emerald-500 border-emerald-500/30 bg-emerald-500/5', icon: CheckCircle2 },
    contradicted: { label: 'CON', color: 'text-destructive border-destructive/30 bg-destructive/5', icon: ShieldAlert },
    absent: { label: 'ABS', color: 'text-amber-600 dark:text-amber-500 border-amber-500/30 bg-amber-500/5', icon: AlertTriangle },
    ambiguous: { label: 'AMB', color: 'text-blue-600 dark:text-blue-400 border-blue-500/30 bg-blue-500/5', icon: Search },
  };

  const config = configs[status] || configs.unverified;
  const Icon = config.icon;

  return (
    <Badge variant="outline" className={`text-[8px] px-1.5 h-4 flex items-center gap-1 font-mono leading-none tracking-tight rounded-none border-[1px] ${config.color}`}>
      <Icon className="w-2 h-2" />
      {config.label}
    </Badge>
  );
}
