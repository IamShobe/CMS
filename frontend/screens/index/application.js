import React from "react";
import {withStyles} from "@material-ui/core";


const styles = {
    application: {
        width: "100px",
        height: "100px",
        cursor: "pointer",
        margin: "12px 30px",
    },
    innerImage: {
        width: "100%",
        height: "100%",
    }
};

class Application extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            image_src: props.image_src,
            callback: props.callback
        }
    }

    componentWillReceiveProps(nextProps, nextContext) {
        return {
            ...this.state,
            image_src: nextProps.image_src,
            callback: nextProps.callback
        }
    }

    render() {
        const {classes} = this.props;
        return (
            <div className={classes.application} onClick={this.state.callback}>
                <img className={classes.innerImage} src={this.state.image_src}/>
            </div>
        );
    }
}

export default withStyles(styles)(Application);