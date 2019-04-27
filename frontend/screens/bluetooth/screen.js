import axios from "axios";
import React from "react";

import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import Avatar from "@material-ui/core/Avatar";
import PhoneIcon from '@material-ui/icons/PhoneIphone';
import List from "@material-ui/core/List";
import ListSubheader from "@material-ui/core/ListSubheader";

import LoadingButton from "../../utils/loading_button";

import "./screen.scss";


export default class BluetoothScreen extends React.Component {

    constructor(props) {
        super(props);
        this.app = props.app;
        this.state = {
            devices: this.props.devices
        };
        this.find_devices = React.createRef();
    }

    componentDidMount() {
        axios.get('/api/bluetooth/devices')
            .then((json) => {
                this.app.updateDevices(json.data);
            });
    }

    findDevices() {
        axios.get('/api/bluetooth/devices/scan')
            .then((json) => {
                this.app.updateDevices(json.data);
                this.find_devices.current.stopLoading();
            });
    }

    componentWillReceiveProps(nextProps, nextContext) {
        this.setState({
            ...this.state,
            ...nextProps
        })
    }

    connectDevice(address) {
        this.app.notification.current.openWithMessage(
            "Should pair with device?",
            `Device address: ${address}`,
            (accepted) => {
                if (accepted) {
                    axios.post('/api/bluetooth/pair', {address: address})
                        .then((json) => {
                            console.log("paring success!");
                        });
                }
            }
        );

    }

    get renderDevices() {
        const devices = [];
        for (const key of Object.keys(this.state.devices)) {
            const dev = this.state.devices[key];
            devices.push(
                <ListItem button key={dev}
                          onClick={() => {
                              this.connectDevice(dev)
                          }}>
                    <ListItemAvatar>
                        <Avatar>
                            <PhoneIcon/>
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                        primary={key}
                        secondary={dev}
                    />
                </ListItem>
            );
        }

        return (
            <List dense={true}
                  style={{
                      flex: 1, overflow: 'auto', backgroundColor: "white",
                      display: "flex", flexDirection: "column"
                  }}
                  subheader={
                      <ListSubheader>Devices</ListSubheader>}>
                {devices.length > 0 ? devices :
                    <div style={{
                        flex: 1,
                        alignItems: "center",
                        justifyContent: "center",
                        display: "flex"
                    }}>
                        <h1>
                            No Devices Exists!
                        </h1>
                    </div>}
            </List>
        );
    }

    get hasDevices() {
        return Object.keys(this.state.devices).length > 0
    }

    render() {

        return (
            <div className="container screen">
                <LoadingButton
                    title={"Scan Devices"}
                    callback={this.findDevices.bind(this)}
                    innerRef={this.find_devices}/>
                <div style={{flex: 1, display: "flex", overflow: "auto"}}>
                    {this.renderDevices}
                </div>
            </div>
        );
    }
}

