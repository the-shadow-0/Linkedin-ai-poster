// src/components/ControlsPanel.js
import React, { useState } from 'react';
import {
    Paper, Box, TextField, Button, Typography
} from '@mui/material';

export default function ControlsPanel({
    draftAvailable,
    onGenerate,
    onPublish,
    publishEnabled,
    loading
}) {
    const [topic, setTopic] = useState('AI in Marketing');

    return (
        <Paper sx={{ p: 3, borderRadius: 2, mb: 4 }}>
            <Typography variant="h5" gutterBottom>
                Generate & Publish LinkedIn Post
            </Typography>
            <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
                <TextField
                    label="Topic"
                    value={topic}
                    onChange={e => setTopic(e.target.value)}
                    sx={{ flex: 1 }}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => onGenerate(topic)}
                    disabled={loading}
                >
                    Generate Draft
                </Button>
                {draftAvailable && (
                    <Button
                        variant="outlined"
                        color="secondary"
                        onClick={onPublish}
                        disabled={!publishEnabled || loading}
                    >
                        {publishEnabled ? 'Publish to LinkedIn' : 'Writing…'}
                    </Button>
                )}
            </Box>
        </Paper>
    );
}
