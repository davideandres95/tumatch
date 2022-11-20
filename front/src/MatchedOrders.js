import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import axios from "axios";
import {getContext} from './Context';

// Generate Order Data
function createData(id, date, name, shipTo, paymentMethod, amount) {
  return { id, date, name, shipTo, paymentMethod, amount };
}


function preventDefault(event) {
  event.preventDefault();
}



export default function Orders() {
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());
  const [order, setOrder] = React.useState('');

  if(order == "") {
    axios.get("/matches", {}).catch((error) => {}).then((response) => {
      if(response != undefined) {
        setOrder(response.data);
      }    
    }); 
  }

  return (
    <React.Fragment>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Security</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {order != "" && order.map((orderr) => (
            <TableRow key={orderr.id}>
              <TableCell>{orderr.created_at}</TableCell>
              <TableCell>{orderr.price}</TableCell>
              <TableCell>{orderr.quantity}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}