import * as React from "react";
import { Redirect } from "react-router-dom";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import * as p from "../Login.css";

interface Props { }

interface State {
  username: string;
  password: string;
  verify_password: string;
  username_helper: string;
  password_helper: string;
  token: string;
}

export default class Register extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { username: "", password: "test", verify_password: "", username_helper: "", password_helper: "", token: "", email: "" };
    this.handleUsername = this.handleUsername.bind(this);
    this.handlePassword = this.handlePassword.bind(this);
    this.handleVerifyPassword = this.handleVerifyPassword.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleEmail = this.handleEmail.bind(this);
  }

  handleEmail(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ email: event.target.value });
  }

  handleUsername(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ username: event.target.value });
  }

  handlePassword(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ password: event.target.value });
  }

  handleVerifyPassword(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ verify_password: event.target.value });
  }

  valid_email = (mail: string) => {
    if (/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
      return (true)
    }
    return (false)
  }


  handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    // if(!this.valid_email(this.state.email)) {
    //   this.setState({username:"",password:"",verify_password:"",username_helper:"Not a valid email  ", password_helper:""});
    // }

    // else if(this.state.password === this.state.verify_password) {
    let data =
      "username=" +
      encodeURIComponent(this.state.username) +
      "&password=" +
      encodeURIComponent(this.state.password);
    // "&email=" +
    // encodeURIComponent(this.state.email)
    fetch(process.env.REACT_APP_BACKEND_URL + `/token/register_easy`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        accept: "application/json",
      },
      body: data,
    })
      .then((res) => res.json())
      .then((result) => {
        if ("access_token" in result) {
          let token = result["access_token"];
          window.sessionStorage.setItem("username", this.state.username);
          window.sessionStorage.setItem("token", token);
          this.setState({ username: this.state.username });
        } else {
          this.setState({ username: "", password: "", verify_password: "", username_helper: "Username or Email already used", password_helper: "" });
        }
      });
    // }
    // else {
    //   this.setState({username_helper: "", password_helper:"Passwords don't match", password:"",verify_password:""});
    // }
    event.preventDefault();
  }

  render() {
    if (window.sessionStorage.getItem("token")) {
      return <Redirect to="/home" />;
    }

    return (
      <Container maxWidth="md">
        <CssBaseline />
        <div className="paper">
          <Avatar className="avatar">
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h4">
            Document Annotation App
          </Typography>
          <form className="form" noValidate onSubmit={this.handleSubmit}>
            {/* <TextField 
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              value={this.state.email}
              onChange={this.handleEmail}
              // helperText={this.state.username_helper}
              autoFocus
            /> */}
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              value={this.state.username}
              onChange={this.handleUsername}
              helperText={this.state.username_helper}
              autoFocus
            />
            {/* <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={this.state.password}
              onChange={this.handlePassword}
              helperText={this.state.password_helper}
            /> */}
            {/* <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="verify_password"
              label="Verify Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={this.state.verify_password}
              onChange={this.handleVerifyPassword}
            /> */}


            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="submit"
            >
              Sign In
            </Button>
            {/* <p>
            <a href="/login" >
                  {"Already have an account? Login "}
                </a>
            </p> */}

            {/* <Grid container className="signup">
              <Grid item xs></Grid>
              <Grid item>
                <a href="/login" className="register">
                  {"Already have an account? Login "}
                </a>
              </Grid>
            </Grid> */}
          </form>
        </div>
      </Container>
    );
  }
}
