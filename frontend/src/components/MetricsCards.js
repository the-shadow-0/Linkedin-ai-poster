import React from 'react';
import {
    Grid, Paper, Typography
} from '@mui/material';

export default function MetricsCards({ metrics }) {
    const items = [
        { label: 'Views', value: metrics.views },
        { label: 'Likes', value: metrics.likes },
        { label: 'Shares', value: metrics.shares },
    ];

    return (
        <Grid container spacing={2}>
            {items.map(item => (
                <Grid item xs={12} md={4} key={item.label}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="h4">{item.value}</Typography>
                        <Typography>{item.label}</Typography>
                    </Paper>
                </Grid>
            ))}
        </Grid>
    );
}
