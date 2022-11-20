import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import Alert from '@mui/material/Alert';
import {getContext} from './Context';

const theme = createTheme();

export default function SignIn() {
  const [state, setState] = React.useState(0);
  const [cpassword, setCPassword] = React.useState("");
  const [error, setError] = React.useState(false);
  const [invalidRegister, setInvalidRegister] = React.useState(false);
  const {isAuth, setAuth, token, setToken} = React.useContext(getContext());

  const validateRegister = (data) => {
    setError(false);
    if (data.get('password') != data.get('cpassword')) {
      setInvalidRegister(true);
      return false;
    } else if (data.get('password').length < 5 || data.get('cpassword').length < 5 || data.get('username').length < 5) {
      setInvalidRegister(true);
      return false;
    }
    return true;
  }

  function handleSubmitRegister (event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (validateRegister(data) == false) {
      return;
    }
    axios.post("auth/register", {
      'username': data.get('username'),
      'password': data.get('password')
    }).catch(() => {setError(true)}).then((response) => {
      if(response == undefined) {
        setError(true) }
      else {
        setError(false);
        setAuth(true);
        setToken(response.data['token'])
      }
    });
  };

  const handleSubmitLogin = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios.post("auth/login", {
      'username': data.get('username'),
      'password': data.get('password')
    }).catch(() => {setError(true)}).then((response) => {
      if(response == undefined) {
        setError(true)
      } else {
        setError(false);
        setAuth(true);
        setToken(response.data['token']);
      }    
    }); 
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      {state == 0 && <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up (Register)
        </Typography>
        <Box component="form" onSubmit={handleSubmitRegister} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="cpassword"
            label="Confirm Password"
            type="password"
            id="cpassword"
            autoComplete="current-password"
          />
          {
            error && <Alert open={error} severity="error">
              Incorrect credentials, or the connection failed.
            </Alert>
          }
          {
            invalidRegister && <Alert open={error} severity="error">
              Incorrect input: len(password) >= 5, len(username) >= 5 and confirm-password==password
            </Alert>
          }

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item>
              <Link href="#" variant="body2" onClick={() => {setState(1);}}>
                {("Have an account? Sign In")}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>}
      {state == 1 && <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in (LogIn)
        </Typography>
        <Box component="form" onSubmit={handleSubmitLogin} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          {
            error && <Alert open={error} severity="error">
              Incorrect credentials, or the connection failed.
            </Alert>
          }
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </Button>
          
          <Grid container>
            <Grid item>
              <Link href="#" variant="body2" onClick={() => {setState(0);}}>
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>}
    </Container>
  );
}