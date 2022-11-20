import * as React from 'react';
import TextField from '@mui/material/TextField';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import axios from 'axios';
import Alert from '@mui/material/Alert';
import {getContext} from './Context';

export default function FormDialog(props) {
  const [op, setOp] = React.useState('ADD');
  const [errorMsg, setErrorMsg] = React.useState("");
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  const performeOperation = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios.post("", {
      'request': 'ADD',
      'side': op,
      'quantity': data.get('quantity'),
      'price': data.get('price'),
      'security': data.get('securities'),
      'user_token': token
    }).catch((error) => {setErrorMsg(error.message)}).then((response) => {
      if(response != undefined) {
        this.close()
      }    
    }); 
  }
  const handleChange = (event) => {
    setOp(event.target.value);
  };

  return (
    <form onSubmit={performeOperation}>
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
              id="quantity"
              name="quantity"
              label="Quantity (integer)"
              fullWidth
              variant="standard"
            />
          </Grid>
          <Grid item xs={12}>
              <TextField
              autoFocus
              margin="dense"
              id="price"
              name="price"
              label="Price (in USD)"
              fullWidth
              variant="standard"
            />
          </Grid>
          <Grid item xs={12}>
              <TextField
              autoFocus
              margin="dense"
              id="securities"
              name="securities"
              label="Securities (e.g.: IBM, APPL)"
              fullWidth
              variant="standard"
            />
          </Grid>
          {
            
            errorMsg != "" && <Grid item xs={12}> 
            <Alert severity="error">
              {errorMsg}
            </Alert>
            </Grid>
          }
          <Grid item xs={12}>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={op}
              label="Operation"
              onChange={handleChange}
            >
              <MenuItem value={'SELL'}>SELL</MenuItem>
              <MenuItem value={'BUY'}>BUY</MenuItem>
            </Select>
          </Grid>
        
        </Grid>
        <DialogActions>
          <Button variant="contained" type="submit">Perform</Button>
        </DialogActions>
      </DialogContent>
    </form>
  );
}