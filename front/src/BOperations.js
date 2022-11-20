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
import SvelteJSONEditor from './SvelteJSONEditor'



export default function FormDialog(props) {
  const [op, setOp] = React.useState('ADD');
  const [errorMsg, setErrorMsg] = React.useState("");
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  const performeOperation = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios.post("", content, {headers: {
      'Content-Type': 'application/json',
    }}).catch((error) => {setErrorMsg(error.message)}).then((response) => {
      if(response != undefined) {
        this.close()
      }    
    }); 
  }
  const handleChange = (event) => {
    setOp(event.target.value);
  };

  const [showEditor, setShowEditor] = React.useState(true);
  const [readOnly, setReadOnly] = React.useState(false);
  const [content, setContent] = React.useState({
    json:
        {
            "user": "Omar",
            "request": "Add",
            "security": "AAPL",
            "quantity": "1000",
            "price": "2",
            "side": "Sell"
        },
    text: undefined
  });

  return (
    <form onSubmit={performeOperation}>
      <DialogTitle>Add batch operation</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Write the operations as a JSON.
        </DialogContentText>
        <div className="my-editor">
            <SvelteJSONEditor
              content={content}
              readOnly={readOnly}
              onChange={setContent}
            />
        </div>
        <div>
          {errorMsg!="" && <Alert severity='error'>{errorMsg}</Alert>}
        </div>
        <DialogActions>
          <Button variant="contained" type="submit">Perform</Button>
        </DialogActions>
      </DialogContent>
    </form>
  );
}