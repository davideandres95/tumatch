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
import Autocomplete from '@mui/material/Autocomplete';

export default function FormDialog(props) {
  const [op, setOp] = React.useState('');
  const [cb, setCb] = React.useState(1);
  const [dataAC, setDataAC] = React.useState("");

  const [errorMsg, setErrorMsg] = React.useState("");
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  const [securities, setSecurities] = React.useState("");
  if(securities == "") {
    axios.get("/securities", {}).catch((error) => {setErrorMsg("Network error")}).then((response) => {
      if(response != undefined) {
        setSecurities(response.data);
      }    
    }); 
  }


  const validate = (data) => {
    console.log(data);
    if(op == '') {
      setErrorMsg("You need to select an operation: BUY / SELL")
      return false;
    } else if (data.get('quantity') <= 0) {
      setErrorMsg("Quantity amount must be positive")
      return false;
    } else if (data.get('price') <= 0 && cb == -1) {
      setErrorMsg("Price must be positive")
      return false;
    } else if (dataAC == "") {
      setErrorMsg("Must select a security")
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
    const price = cb == -1 ? data.get('price') : "MARKET";
    axios.post("/order", {
      "AddOrderRequest" : [
        {
        'request': 'ADD',
        'side': op,
        'quantity': data.get('quantity'),
        'price': price,
        'security': dataAC,
        'user_token': token
        }
      ]
    }).catch((error) => {setErrorMsg(error.message)}).then((response) => {
      if(response != undefined) {
        props.value(false);
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
            <Grid item xs={6} sx={{'marginTop': 3}}>
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
          <Grid item container xs={12}>
            <Grid item container xs={6}>
              <p>Security:</p>
              <Autocomplete
                disablePortal
                onChange={(event) => setDataAC(event.target.outerText)}
                id="securities"
                options={securities}
                sx={{ width: 150, 'marginLeft': 1 }}
                renderInput={(params) => <TextField {...params} label="Securities" />}
              />
            </Grid>
            <Grid item xs={6}>
              Operation: 
              <Select
                sx={{'marginLeft': 1}}
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
          {
            
            errorMsg != "" && <Grid item xs={12}> 
            <Alert severity="error">
              {errorMsg}
            </Alert>
            </Grid>
          }
        </Grid>
        <DialogActions>
          <Button variant="contained" type="submit">Perform</Button>
        </DialogActions>
      </DialogContent>
    </form>
  );
}