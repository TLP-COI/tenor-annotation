import React, { useState, useEffect } from 'react';

import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import { Redirect, Link } from 'react-router-dom';

import Tutorial from './Tutorial.jsx';
import {postRequest, getRequest} from '../utils';

// import useStyles from './Styles';

const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
  }));

  
  
export default function Navbar(props) {
    const classes = useStyles();

    // function calculateTimeLeft() {
    //     if (props.endDateTime) {
    //         let timeLeft = new Date(props.endDateTime) - new Date() // TODO: timezones
    //         // console.log('timeLeft', Math.trunc(timeLeft / 60000))
    //         return `Time Remaining: ${Math.trunc(timeLeft / 60000)} Minutes`
    //     } else {
    //         return ""
    //     }
    // }
    // const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());
  
    // useEffect(() => {
    //   const timer = setTimeout(() => {
    //     setTimeLeft(calculateTimeLeft());
    //   }, 1000);
    //   return () => clearTimeout(timer);
    // });

    let logout = (e) => {
        window.sessionStorage.clear("token");
        // return <Redirect to="/login" />;
    }

    
    return (

        <div className={classes.root} id="navbar">

            <AppBar position="fixed">
                <Toolbar>
                    {/* <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                        <MenuIcon />
                    </IconButton> */}
                    <Typography variant="h6" className={classes.title}>
                        {/* {props.text} */}
                        Document Annotation App
                    </Typography>

                    {/* time left in minutes */}
                    {/* {new Date(props.endDateTime)} */}

                    <Tutorial />
                    {/* {props.tutorial} */}
                        
                    <Link to="/table_view">
                        <Button variant="contained" color="primary" disableElevation>
                            Table View
                        </Button>
                    </Link>
                    <Link to="/">
                        <Button variant="contained" color="primary" disableElevation>
                            Dashboard
                        </Button>
                    </Link>
                    <Link to="/home">
                        <Button variant="contained" color="primary" disableElevation>
                            Home
                        </Button>
                    </Link>
                    {/* <Button variant="contained" color="primary" disableElevation onClick={reset}>
                        Reset session
                    </Button> */}
                    
                    <Link to="/register">
                        <Button onClick={logout} variant="contained" color="primary" disableElevation>
                            Logout
                        </Button>
                    </Link>

                </Toolbar>
            </AppBar>
        </div>
    )
}