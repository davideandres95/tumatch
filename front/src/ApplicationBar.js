import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Operation from './Operation';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import {getContext} from './Context';
import Grid from '@mui/material/Grid';
import BOperations from './BOperations';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { JSONEditor } from 'svelte-jsoneditor'


export default function ApplicationBar() {
  const [open, setOpen] = React.useState(false);
  const [bopen, setBOpen] = React.useState(false);

  const [openToken, setOpenToken] = React.useState(false);

  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            TUMatcher
          </Typography>
          { isAuth && 
          <Box>
            <Button  style={{margin:5}} variant="contained" onClick = {() => {setOpenToken(true);}}>Token</Button>
            <Button  style={{margin:5}} variant="contained" onClick = {() => {setOpen(true);}}>Add Operation</Button>
            <Button  style={{margin:5}} variant="contained" onClick = {() => {setBOpen(true);}}>Batch Operations (JSON)</Button>
            <Button  style={{margin:5}} variant="contained" onClick = {() => {setAuth(false); setToken("");}}>Log Out</Button>
          </Box>
          }
        </Toolbar>
      </AppBar>
      <Dialog open={open} fullWidth onClose={() => setOpen(false)}>
        <Operation value={setOpen}/>
      </Dialog>
      <Dialog open={bopen} fullWidth onClose={() => setBOpen(false)}>
        <BOperations/>
      </Dialog>
      <Dialog open={openToken} fullWidth onClose={() => setOpenToken(false)}>
        <DialogTitle>APIs token (WebSocket: /websocket/$token)</DialogTitle>
        <DialogContent>{token}</DialogContent>
      </Dialog>
    </Box>
  );
}