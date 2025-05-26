// src/components/DraftPreview.js
import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

export default function DraftPreview({ draft }) {
    if (!draft) return null;
    return (
        <Paper sx={{ p: 3, background: '#f0f5f9', mb: 4 }}>
            <Typography variant="h6" gutterBottom>
                Draft Preview
            </Typography>
            <Box
                component="pre"
                sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}
            >
                {draft}
            </Box>
        </Paper>
    );
}
