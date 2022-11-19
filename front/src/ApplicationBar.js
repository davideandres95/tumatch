import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Operation from './Operation';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';

export default function ApplicationBar() {
  const [open, setOpen] = React.useState(false);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            TUMacher
          </Typography>
          <Button variant="contained" onClick = {() => {setOpen(true);}}>Add Operation</Button>
        </Toolbar>
      </AppBar>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <Operation/>
        <DialogActions>
          <Button variant="contained" onClick={() => setOpen(0)}>BUY</Button>
          <Button variant="contained" onClick={() => setOpen(0)}>SELL</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}