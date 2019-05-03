import React from "react";
import io from 'socket.io-client';

import AlertDialogSlide from "./utils/notification";

import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import {withStyles} from '@material-ui/core/styles';

import BackIcon from '@material-ui/icons/ArrowBackIosOutlined';
import BluetoothIcon from '@material-ui/icons/SettingsBluetoothOutlined';
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
import DevicesManager from "./structures/devices_manager";

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
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    fabOptions: {
        position: 'absolute',
        zIndex: 1,
        top: -30,
        left: 0,
        right: 0,
        width: 200,
        margin: '0 auto',
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        "& *": {
            zIndex: 1
        }
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
            selectedScreen: "Index",
            screensStack: ["Index"],
            buttons: []
        };
        this.socket = io();
        this.nsp = io('/client', {forceNew: true});
        this.bindSocket();

        this.notification = React.createRef();

        this.bluetoothScreen = <BluetoothScreen app={this}
                                                searchDevices={this.searchDevices}
        />;

        this.phonebookScreen = <PhoneBookScreen app={this}/>;
        this.indexScreen = <IndexScreen app={this}/>;
    }

    bindSocket() {
        this.socket.on('connect', function () {
            console.log("connected!")
        });
        this.socket.on('event', function (data) {
            console.log(`event:`, data)
        });
        this.socket.on('message', function (data) {
            console.log(`message:`, data)
        });
        this.nsp.on('pairing_request', (data) => {
            console.log(`paring:`, data);
            console.log('address:', data.mac_address);
            this.notification.current.openWithMessage(
                "Should pair with device?",
                `device name: ${data.name}\n` +
                `address: ${data.mac_address}\n` +
                `pin code: ${data.pin_code[0]}`,
                (accepted) => {
                    this.nsp.emit("pair_response", {
                        address: data.mac_address,
                        accepted: accepted
                    });
                }
            );
        });
        this.socket.on('disconnect', function () {
            console.log("disconnected!")
        });
        this.socket.on('bg_emit', function (data) {
            console.log(`bg emitting:`, data)
        });
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
            screensStack: newStack,
            buttons: []
        })
    }

    renderScreen() {
        switch (this.state.selectedScreen) {
            case "Bluetooth":
                return this.bluetoothScreen;
            case "Contacts":
                return this.phonebookScreen;

            default:
                return this.indexScreen;
        }
    }

    setButtons(buttons) {
        this.setState({
            ...this.state,
            buttons: buttons
        })
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
                        <div className={classes.fabOptions}>
                            {this.state.buttons}
                        </div>
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
