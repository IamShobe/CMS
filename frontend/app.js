import React from "react";
import io from 'socket.io-client';

import AlertDialogSlide from "./utils/notification";

import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import ReactCSSTransitionGroup from 'react-addons-css-transition-group'; // ES6
import {withStyles} from '@material-ui/core/styles';

import Fab from '@material-ui/core/Fab';
import BackIcon from '@material-ui/icons/ArrowBackIosOutlined';
import BluetoothIcon from '@material-ui/icons/SettingsBluetoothOutlined';
import SearchIcon from '@material-ui/icons/Search';
import MoreIcon from '@material-ui/icons/MoreVert';
import Typography from "@material-ui/core/Typography";
import Clock from 'react-live-clock';

import BluetoothScreen from "./screens/bluetooth/screen";
import PhoneBookScreen from "./screens/phonebook/screen";
import IndexScreen from "./screens/index/screen";
import TransitionGroup from "react-transition-group/TransitionGroup";

import CSSTransition from "react-transition-group/CSSTransition";
import "./style.scss";
import "./test_transitions.scss";

const styles = theme => ({
    text: {
        paddingTop: theme.spacing.unit * 2,
        paddingLeft: theme.spacing.unit * 2,
        paddingRight: theme.spacing.unit * 2,
    },
    paper: {
        paddingBottom: 50,
    },
    list: {
        marginBottom: theme.spacing.unit * 2,
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
    subHeader: {
        backgroundColor: theme.palette.background.paper,
    },
    appBar: {
        top: 'auto',
        bottom: 0
    },
    spacer: {
        flex: 1
    },
    toolbar: {
        // alignItems: 'center',
        // justifyContent: 'space-between',
    },
    fabButton: {
        position: 'absolute',
        zIndex: 1,
        top: -30,
        left: 0,
        right: 0,
        margin: '0 auto',
    },
});

const transitionClassName = "container";
const pageTransitionName = "page";
const transitionDuration = 300;
const transitionEnterTimeout = 2 * transitionDuration;


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            book: [],
            devices: {},
            selectedScreen: "Index",
            screensStack: ["Index"]
        };
        const socket = io();
        const nsp = io('/client', {forceNew: true});

        this.notification = React.createRef();
        // this.find_devices = React.createRef();
        // this.manager = new Manager();
        // this.devices_track = 0;

        socket.on('connect', function () {
            console.log("connected!")
        });
        socket.on('event', function (data) {
            console.log(`event:`, data)
        });
        socket.on('message', function (data) {
            console.log(`message:`, data)
        });
        nsp.on('pairing_request', (data) => {
            console.log(`paring:`, data);
            console.log('address:', data.mac_address);
            this.notification.current.openWithMessage(
                "Should pair with device?",
                `device name: ${data.name}\n` +
                `address: ${data.mac_address}\n` +
                `pin code: ${data.pin_code[0]}`,
                (accepted) => {
                    nsp.emit("pair_response", {
                        address: data.mac_address,
                        accepted: accepted
                    });
                }
            );
        });
        socket.on('disconnect', function () {
            console.log("disconnected!")
        });
        socket.on('bg_emit', function (data) {
            console.log(`bg emitting:`, data)
        });
        this.socket = socket;
    }


    updateDevices(devices) {
        this.setState({
            ...this.state,
            devices: devices
        })
    }

    selectScreen(screenName) {
        if (this.lastScreen === screenName) {
            return
        }
        const newStack = [...this.state.screensStack];
        let index = newStack.indexOf(screenName);
        if (index > -1) {
            newStack.splice(index, 1);
        }
        newStack.push(screenName);

        this.setState({
            ...this.state,
            selectedScreen: screenName,
            screensStack: newStack
        })
    }

    get lastScreen() {
        return this.state.screensStack[this.state.screensStack.length - 1]
    }

    goBack() {
        const stack = this.state.screensStack;
        const newStack = [...stack];
        newStack.pop();
        const new_screen = newStack[newStack.length - 1];
        this.setState({
            ...this.state,
            selectedScreen: new_screen,
            screensStack: newStack
        })
    }

    renderScreen() {
        switch (this.state.selectedScreen) {
            case "Bluetooth":
                return <BluetoothScreen app={this}
                                        devices={this.state.devices}/>;
            case "Contacts":
                return <PhoneBookScreen app={this}/>;

            default:
                return <IndexScreen app={this}/>;
        }
    }

    hasStack() {
        return this.state.screensStack.length > 1;
    }

    renderBack() {
        if (this.hasStack()) {
            return <IconButton color="inherit" onClick={() => {
                this.goBack();
            }}>
                <BackIcon/>
            </IconButton>
        }
    }

    render() {
        const {classes} = this.props;
        return (
            <div className="container">
                {/*<Phonebook book={this.state.book}/>*/}

                <TransitionGroup className="transition-group">
                    <CSSTransition
                        key={this.state.selectedScreen}
                        classNames='page'
                        timeout={100}
                    >
                        {this.renderScreen()}
                    </CSSTransition>
                </TransitionGroup>

                <AlertDialogSlide ref={this.notification}/>

                <AppBar position="relative" color="primary"
                        className={classes.appBar}>
                    <Toolbar className={classes.toolbar}>
                        {this.renderBack()}
                        <Typography className={classes.title} variant="h6"
                                    color="inherit" noWrap>
                            {this.state.selectedScreen}
                        </Typography>
                        <div className={classes.spacer}/>
                        {/*<Fab color="secondary" aria-label="Add"*/}
                        {/*     className={classes.fabButton}>*/}
                        {/*    <AddIcon/>*/}
                        {/*</Fab>*/}
                        <div>
                            <IconButton color="inherit" onClick={() => {
                                this.selectScreen("Bluetooth")
                            }}>
                                <BluetoothIcon/>
                            </IconButton>
                            <IconButton color="inherit">
                                <MoreIcon/>
                            </IconButton>
                            <Clock/>
                        </div>
                    </Toolbar>
                </AppBar>
            </div>
        );
    }
}

export default withStyles(styles)(App);
