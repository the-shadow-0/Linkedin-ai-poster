// src/App.js
import React, { useState, useEffect } from 'react';
import {
  Container,
  CssBaseline,
  ThemeProvider,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import theme from './theme';
import ControlsPanel from './components/ControlsPanel';
import DraftPreview from './components/DraftPreview';
import MetricsCards from './components/MetricsCards';
import MetricsChart from './components/MetricsChart';
import { generateDraft, publishDraft, fetchMetrics } from './api';

function App() {
  const [rawDraft, setRawDraft] = useState('');
  const [displayedDraft, setDisplayedDraft] = useState('');
  const [animationDone, setAnimationDone] = useState(false);

  const [postUrl, setPostUrl] = useState('');
  const [metrics, setMetrics] = useState({ views: 0, likes: 0, shares: 0 });
  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(false);   // API call in-flight
  const [typing, setTyping] = useState(false);     // Typewriter in-flight
  const [error, setError] = useState('');

  // Typewriter effect: runs when rawDraft changes
  useEffect(() => {
    if (!rawDraft) return;

    setDisplayedDraft('');
    setAnimationDone(false);
    setTyping(true);

    let idx = 0;
    const speedMs = 15;
    const timer = setInterval(() => {
      setDisplayedDraft(prev => prev + rawDraft.charAt(idx));
      idx++;
      if (idx >= rawDraft.length) {
        clearInterval(timer);
        setTyping(false);
        setAnimationDone(true);
      }
    }, speedMs);

    return () => clearInterval(timer);
  }, [rawDraft]);

  // Handle Generate button
  const handleGenerate = async (topic) => {
    setError('');
    setLoading(true);
    setRawDraft('');  // clear any previous draft
    try {
      const draft = await generateDraft(topic);
      setRawDraft(draft);
      // reset publish/metrics state
      setPostUrl('');
      setMetrics({ views: 0, likes: 0, shares: 0 });
      setHistory([]);
    } catch (e) {
      console.error(e);
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle Publish button
  const handlePublish = async () => {
    setError('');
    setLoading(true);
    try {
      const url = await publishDraft(rawDraft);
      setPostUrl(url);
      const urn = url.split('/').pop();
      const m = await fetchMetrics(urn);
      setMetrics(m);
      setHistory(hist => [
        ...hist,
        { time: new Date().toLocaleTimeString(), ...m }
      ]);
    } catch (e) {
      console.error(e);
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container sx={{ py: 4 }}>

        {/* Error Banner */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {/* Controls */}
        <ControlsPanel
          draftAvailable={!!rawDraft}
          onGenerate={handleGenerate}
          onPublish={handlePublish}
          publishEnabled={animationDone && !loading && !typing}
          loading={loading || typing}
        />

        {/* Spinner: either generating or typing */}
        {(loading || typing) && (
          <Box textAlign="center" my={4}>
            <CircularProgress />
            <Box mt={2}>
              {loading
                ? 'Generating draft… please wait.'
                : 'Writing post… stay tuned.'}
            </Box>
          </Box>
        )}

        {/* Draft Preview */}
        <DraftPreview draft={displayedDraft} />

        {/* Metrics */}
        {postUrl && (
          <Box mt={4}>
            <MetricsCards metrics={metrics} />
            <Box mt={4}>
              <MetricsChart data={history} />
            </Box>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
