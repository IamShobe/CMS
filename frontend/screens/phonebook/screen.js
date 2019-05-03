import axios from "axios";

import React from "react";

import {withStyles} from "@material-ui/core";
import "./screen.scss";
import Phonebook from "./phonebook";
import bluetooth from "../../structures/devices_manager";


const styles = {
};

class PhoneBookScreen extends React.Component {

    constructor(props) {
        super(props);
        this.app = props.app;
        this.state = {
            book: []
        }

    }

    // componentDidMount(){
    //     axios.get('/static/phonebook.json')
    //         .then((json) => {
    //
    //             // The data from the request is available in a .then block
    //             // We return the result using resolve.
    //             console.log(json.data);
    //             this.setState({
    //                 ...this.state,
    //                 book: json.data
    //             })
    //         });
    // }

    render() {
        const {classes} = this.props;
        return (

            <div className="container screen">
                <Phonebook book={bluetooth.phonebook}/>
            </div>
        );
    }
}

export default withStyles(styles)(PhoneBookScreen);