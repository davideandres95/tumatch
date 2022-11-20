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
import Checkbox from '@mui/material/Checkbox';

export default function FormDialog(props) {
  const [op, setOp] = React.useState('');
  const [cb, setCb] = React.useState(1);

  const [errorMsg, setErrorMsg] = React.useState("");
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  const validate = (data) => {
    console.log(data);
    if(op == '') {
      setErrorMsg("You need to select an operation: BUY / SELL")
      return false;
    } else if (data.get('quantity') <= 0) {
      setErrorMsg("Quantity amount must be positive")
      return false;
    } else if (data.get('price') <= 0 && cb == 1) {
      setErrorMsg("Price must be positive")
      return false;
    } else if (data.get('securities').length <= 2) {
      setErrorMsg("Security length must be longer than 2")
      return false
    }
    return true;
  }

  const performeOperation = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if(validate(data) == false){
      return;
    }
    const price = cb == 1 ? data.get('price') : "MARKET";
    axios.post("", {
      'request': 'ADD',
      'side': op,
      'quantity': data.get('quantity'),
      'price': price,
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
        <Grid container spacing={1}>
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
          <Grid item container xs={12}>
            <Grid item xs={6} sx={{'margin-top': 20}}>
              Default Market price: 
              <Checkbox defaultChecked onChange={()=>{setCb(cb*-1)}} />
            </Grid>
            <Grid item xs={6}>
              <TextField
              disabled={cb == 1}
              autoFocus
              margin="dense"
              id="price"
              name="price"
              label="Price (in USD)"
              fullWidth
              variant="standard"
              />
            </Grid>
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