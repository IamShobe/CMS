import axios from "axios";
import React from "react";

import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import Avatar from "@material-ui/core/Avatar";
import PhoneIcon from '@material-ui/icons/PhoneIphone';
import PairIcon from '@material-ui/icons/Phonelink';
import ConnectIcon from '@material-ui/icons/BluetoothConnected';
import DisconnectIcon from '@material-ui/icons/BluetoothDisabled';
import List from "@material-ui/core/List";
import ListSubheader from "@material-ui/core/ListSubheader";

import LoadingIcon from "../../utils/loading_icon";

import "./screen.scss";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import IconButton from "@material-ui/core/IconButton";
import SearchIcon from '@material-ui/icons/Search';
import RefreshIcon from '@material-ui/icons/Refresh';
import DeleteIcon from '@material-ui/icons/Delete';
import ServicesTable from "./services";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import bluetooth from "../../structures/devices_manager";

let state = {
    renderAck: -1,
    selectedServices: [],
    selectedDevice: null,
    reachable: {}
};

export default class BluetoothScreen extends React.Component {

    constructor(props) {
        super(props);
        this.app = props.app;
        this.state = state;
        this.find_devices = React.createRef();
        this.refresh_devices = React.createRef();
        this.prev_list = undefined;
        this.renderAck = this.state.renderAck;
        this.lock = false;
    }

    componentDidMount() {
        this.updateStatus();
        this.searchDevices = (
            <LoadingIcon key={"findDevices"}
                         normal_icon={<SearchIcon/>}
                         callback={this.findDevices.bind(this)}
                         innerRef={this.find_devices}
            />);
        this.refreshDevices = (
            <LoadingIcon key={"refresh"}
                         normal_icon={<RefreshIcon/>}
                         callback={this.updateStatus.bind(this)}
                         innerRef={this.refresh_devices}
            />);
        this.app.setButtons([this.searchDevices, this.refreshDevices]);
    }

    componentWillUnmount() {
        // Remember state for the next mount
        state = {
            ...this.state,
            renderAck: this.renderAck
        };
    }

    updateStatus(keepSelectedDevice = true) {
        if (this.lock)
            return;

        this.lock = true;
        let pairable = axios.get('/api/bluetooth/devices/pairable');
        let paired = axios.get('/api/bluetooth/devices/paired');
        let connected = axios.get('/api/bluetooth/devices/connected');
        let base_status = Promise.all([pairable, paired, connected]).then(
            (values) => {
                let [pairable, paired, connected] = values;
                bluetooth.update({
                    pairable: pairable.data,
                    paired: paired.data,
                    connected: connected.data
                });
                this.setState({
                    ...this.state,
                    selectedDevice: keepSelectedDevice ? this.state.selectedDevice : null
                });
            }
        );

        this.available = axios.get('/api/bluetooth/devices/available');

        Promise.all([base_status, this.available]).then((value) => {
            let [, available] = value;
            let to_ret = {};
            for (let device of available.data) {
                if (device.alive) {
                    to_ret[device.mac_address] = device;
                }
            }
            this.setState({
                ...this.state,
                reachable: to_ret,
                selectedDevice: keepSelectedDevice ? this.state.selectedDevice : null
            });
            this.refresh_devices.current.stopLoading();
            this.lock = false;
        });
    }

    findDevices() {
        axios.get('/api/bluetooth/devices/scan')
            .then((json) => {
                this.find_devices.current.stopLoading();
                this.updateStatus();
            });
    }

    pairDevice(address) {
        this.app.notification.current.openWithMessage(
            "Should pair with device?",
            `Device address: ${address}`,
            (accepted) => {
                if (accepted) {
                    axios.post(`/api/bluetooth/devices/${address}/pair/`)
                        .then((json) => {
                            console.log("paring success!");
                            axios.post(`/api/bluetooth/devices/${address}/disconnect/`)
                                .then((json) => {
                                    console.log("disconnection success!");
                                    this.updateStatus();
                                });
                        });
                }
            }
        );
    }

    connectDevice(address) {
        this.app.notification.current.openWithMessage(
            "Should connect to device?",
            `Device address: ${address}`,
            (accepted) => {
                if (accepted) {
                    let last_device = this.state.connectedDevice;
                    if (last_device) {
                        // TODO: disconnect previous
                    }

                    axios.post(`/api/bluetooth/devices/${address}/connect/`)
                        .then((json) => {
                            console.log("connection success!");
                            this.updateStatus();
                            axios.get(`/api/bluetooth/devices/${address}/phonebook/`)
                                .then(
                                    (json) => {
                                        bluetooth.updatePhoneBook(json.data);
                                        console.log(json.data)
                                    }
                                );
                        });
                }
            }
        );
    }

    disconnectDevice(address) {
        this.app.notification.current.openWithMessage(
            "Should disconnect from device?",
            `Device address: ${address}`,
            (accepted) => {
                axios.post(`/api/bluetooth/devices/${address}/disconnect/`)
                    .then((json) => {
                        console.log("disconnection success!");
                        this.updateStatus();
                    });
            });
    }


    removeDevice(address) {
        this.app.notification.current.openWithMessage(
            "Should remove device?",
            `Device address: ${address}`,
            (accepted) => {
                axios.post(`/api/bluetooth/devices/${address}/remove/`)
                    .then((json) => {
                        console.log("remove success!");
                        this.updateStatus(false);
                    });
            });
    }

    getServices(address) {
        this.setState({
            ...this.state,
            selectedServices: [],
            selectedDevice: address
        });
        axios.get(`/api/bluetooth/devices/${address}/services/`)
            .then((json) => {
                if (this.state.selectedDevice === address) {
                    this.setState({
                        ...this.state,
                        selectedServices: json.data.services
                    });
                }
            }).catch((error) => {
            if (this.state.selectedDevice === address) {
                this.updateStatus(false);
            } else {
                this.updateStatus();
            }
        });

    }

    renderSubDevices(data, action, icon, action2, icon2) {
        const devices = [];
        for (const key of Object.keys(data)) {
            const dev = data[key];
            devices.push(
                <ListItem button key={dev.mac_address} onClick={() => {
                    this.getServices(dev.mac_address)
                }} disabled={!(dev.mac_address in this.state.reachable)}>
                    <ListItemAvatar>
                        <Avatar>
                            <PhoneIcon/>
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                        primary={dev.name}
                        secondary={dev.mac_address}
                    />

                    <ListItemSecondaryAction>
                        {action ?
                            <IconButton onClick={() => {
                                action(dev.mac_address)
                            }}
                                        disabled={!(dev.mac_address in this.state.reachable)}>
                                {icon}
                            </IconButton> : undefined}
                        {action2 ?
                            <IconButton onClick={() => {
                                action2(dev.mac_address)
                            }}>
                                {icon2}
                            </IconButton> : undefined}
                    </ListItemSecondaryAction>
                </ListItem>
            );
        }
        if (devices.length > 0)
            return devices;
    }

    get renderDevices() {
        // if (this.renderAck === bluetooth.renderAck)
        //     return this.prev_list;
        // this.renderAck++;

        const connected_devices = this.renderSubDevices(
            bluetooth.connected,
            this.disconnectDevice.bind(this),
            <DisconnectIcon/>);
        const paired_devices = this.renderSubDevices(
            bluetooth.paired,
            this.connectDevice.bind(this),
            <ConnectIcon/>,
            this.removeDevice.bind(this),
            <DeleteIcon/>);
        const topair_devices = this.renderSubDevices(
            bluetooth.to_pair,
            this.pairDevice.bind(this),
            <PairIcon/>);
        this.prev_list = (
            <List dense={true}
                  style={{
                      flex: 1, overflow: 'auto', backgroundColor: "white",
                      display: "flex", flexDirection: "column"
                  }}
                  subheader={<ListSubheader/>}>
                <ListSubheader>Connected Devices</ListSubheader>
                {connected_devices}
                <ListSubheader>Paired Devices</ListSubheader>
                {paired_devices}
                <ListSubheader>Available Devices</ListSubheader>
                {topair_devices}
            </List>
        );
        return this.prev_list;
    }

    get hasDevices() {
        return Object.keys(bluetooth.devices).length > 0
    }

    get renderDetails() {
        if (this.state.selectedDevice === null)
            return;
        return (
            <React.Fragment>
                <div style={{display: "flex"}}>
                    <Avatar style={{margin: "10px"}}>
                        <PhoneIcon/>
                    </Avatar>
                    <div>
                        <Typography component="h5" variant="h5">
                            {bluetooth.address_to_name[this.state.selectedDevice]}
                        </Typography>
                        <Typography variant="subtitle1" color="textSecondary">
                            {this.state.selectedDevice}
                        </Typography>
                    </div>
                </div>
                <Divider/>
                <Typography
                    variant="h6"
                    id="tableTitle">
                    Available
                    Services
                </Typography>
                <div style={{flex: 1}}>
                    <ServicesTable
                        rowCount={this.state.selectedServices.length}
                        rowGetter={({index}) => this.state.selectedServices[index]}
                        onRowClick={event => console.log(event)}
                        columns={[
                            {
                                width: 100,
                                flexGrow: 1.0,
                                label: 'Name',
                                dataKey: 'name',
                            },
                            {
                                width: 100,
                                label: 'Protocol',
                                dataKey: 'protocol',
                            },
                            {
                                width: 100,
                                label: 'Port',
                                dataKey: 'port',
                                numeric: true,
                            }
                        ]}/>
                </div>
            </React.Fragment>
        );
    }

    render() {
        return (
            <div className="container screen">
                <div style={{flex: 1, display: "flex", overflow: "auto"}}>
                    {this.renderDevices}
                    <div style={{
                        flex: this.state.selectedDevice ? 1 : 0,
                        display: "flex",
                        flexDirection: "column",
                        margin: "10px 0 0 10px",
                        transition: "flex 0.2s ease"
                    }}>
                        {this.renderDetails}
                    </div>
                </div>
            </div>
        );
    }
}

