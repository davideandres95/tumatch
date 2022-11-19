import * as React from 'react';
import TextField from '@mui/material/TextField';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';

export default function FormDialog() {

  return (
    <div>
      <DialogTitle>Add operation</DialogTitle>
      <DialogContent>
        <DialogContentText>
          The operations are: BUY, SELL
        </DialogContentText>
        <Grid container spacing={3}>
          <Grid item xs={12}>
              <TextField
              autoFocus
              margin="dense"
              id="securities"
              label="Securities (e.g.: IBM, APPL)"
              fullWidth
              variant="standard"
            />
          </Grid>
          <Grid item xs={12}>
              <TextField
              autoFocus
              margin="dense"
              id="price"
              label="Price (in USD)"
              fullWidth
              variant="standard"
            />
          </Grid>
        </Grid>

      </DialogContent>
    </div>
  );
}