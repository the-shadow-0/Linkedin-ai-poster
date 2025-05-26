import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: { main: '#005f73' },
        secondary: { main: '#ee9b00' },
        background: { default: '#e0fbfc' },
    },
    typography: { fontFamily: '"Poppins", sans-serif' },
});

export default theme;
