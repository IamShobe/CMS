import React from "react";

import Application from "./application";
import phonebook_icon from "./system_contacts.png";
import music_icon from "./music_icon.png";

import {withStyles} from "@material-ui/core";
import "./screen.scss";


const styles = {
    app_drawer: {
        display: "flex",
        padding: "20px 0px",
        // flex: 1,
        flexWrap: "wrap",
        justifyContent: "space-between",
        // alignItems: "center",
        "&::after": {
            content: "''",
            flex: "auto"
        },
        overflow: "hidden"
    },
    spacer: {
        // flex: 1
    }
};

class IndexScreen extends React.Component {

    constructor(props) {
        super(props);
        this.app = props.app;
    }

    render() {
        const {classes} = this.props;
        return (

            <div className="container screen">
                <div className={classes.app_drawer}>
                    <Application image_src={phonebook_icon} name={"Contacts"}
                                 callback={() => {
                                     this.app.selectScreen("Contacts")
                                 }}/>
                    <Application image_src={music_icon} name={"Music"}
                                 callback={() => {
                                     this.app.selectScreen("Music")
                                 }}/>
                    {/*<div className={classes.spacer}></div>*/}
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(IndexScreen);