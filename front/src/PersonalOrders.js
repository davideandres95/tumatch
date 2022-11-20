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

const rows = [
  createData(
    0,
    '16 Mar, 2019',
    'Elvis Presley',
    'Tupelo, MS',
    'VISA ⠀•••• 3719',
    312.44,
  ),
  createData(
    1,
    '16 Mar, 2019',
    'Paul McCartney',
    'London, UK',
    'VISA ⠀•••• 2574',
    866.99,
  ),
  createData(2, '16 Mar, 2019', 'Tom Scholz', 'Boston, MA', 'MC ⠀•••• 1253', 100.81),
  createData(
    3,
    '16 Mar, 2019',
    'Michael Jackson',
    'Gary, IN',
    'AMEX ⠀•••• 2000',
    654.39,
  ),
  createData(
    4,
    '15 Mar, 2019',
    'Bruce Springsteen',
    'Long Branch, NJ',
    'VISA ⠀•••• 5919',
    212.79,
  ),
];

function preventDefault(event) {
  event.preventDefault();
}



export default function Orders() {
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());
  const [order, setOrder] = React.useState('');

  if(order == "") {
    axios.post("/order", {
      "ListOrdersRequest" : [
        {
          'request': 'list',
          'user_token': token
        }
      ]
    }).catch((error) => {}).then((response) => {
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
            <TableCell>Side</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {order != "" && order.map((orderr) => (
            <TableRow key={orderr.id}>
              <TableCell>{orderr.created_at}</TableCell>
              <TableCell>{orderr.price}</TableCell>
              <TableCell>{orderr.quantity}</TableCell>
              <TableCell>{orderr.security_id}</TableCell>
              <TableCell>{orderr.side == 1 ? "BUY" : "SELL"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}