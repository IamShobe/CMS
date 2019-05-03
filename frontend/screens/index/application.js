import React from "react";
import {withStyles} from "@material-ui/core";


const styles = {
    application: {
        cursor: "pointer",
        margin: "12px 30px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center"
    },
    innerImage: {
        width: "100px",
        height: "100px",
    },
    name: {
        margin: 5

    }
};

class Application extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            image_src: props.image_src,
            name: props.name,
            callback: props.callback
        }
    }

    componentWillReceiveProps(nextProps, nextContext) {
        return {
            ...this.state,
            image_src: nextProps.image_src,
            name: nextProps.name,
            callback: nextProps.callback
        }
    }

    render() {
        const {classes} = this.props;
        return (
            <div className={classes.application} onClick={this.state.callback}>
                <img className={classes.innerImage} src={this.state.image_src}/>
                <div className={classes.name}>{this.state.name}</div>
            </div>
        );
    }
}

export default withStyles(styles)(Application);