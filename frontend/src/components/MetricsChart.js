import React from 'react';
import {
    Paper, Typography
} from '@mui/material';
import {
    ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip
} from 'recharts';

export default function MetricsChart({ data }) {
    if (!data.length) return null;
    return (
        <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
                Metrics Over Time
            </Typography>
            <ResponsiveContainer width="100%" height={250}>
                <LineChart data={data}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="views" stroke="#005f73" dot={false} />
                    <Line type="monotone" dataKey="likes" stroke="#ee9b00" dot={false} />
                    <Line type="monotone" dataKey="shares" stroke="#9b2226" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </Paper>
    );
}
