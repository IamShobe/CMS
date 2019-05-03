import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import {withStyles} from '@material-ui/core/styles/index';
import CircularProgress from '@material-ui/core/CircularProgress/index';
import green from '@material-ui/core/colors/green';
import Button from '@material-ui/core/Button/index';
import CheckIcon from '@material-ui/icons/Check';
import Fab from "@material-ui/core/Fab";


const styles = theme => ({
    root: {
        display: 'inline-flex',
        alignItems: 'center',
    },
    wrapper: {
        margin: theme.spacing.unit,
        position: 'relative',
    },
    // buttonSuccess: {
    //     backgroundColor: green[500],
    //     '&:hover': {
    //         backgroundColor: green[700],
    //     },
    // },
    buttonProgress: {
        color: green[500],
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -12,
        marginLeft: -12,
    },
    fabProgress: {
        color: green[500],
        position: 'absolute',
        top: -6,
        left: -6,
        zIndex: 1,
    },
});

class LoadingIcon extends React.Component {
    state = {
        loading: false,
        success: false,
    };

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            callback: props.callback,
            success_icon: <CheckIcon/>,
            normal_icon: props.normal_icon
        }
    }

    stopLoading() {
        this.setState({
            ...this.state,
            loading: false,
            success: true,
        });
    }

    handleButtonClick = () => {
        if (!this.state.loading) {
            this.setState(
                {
                    ...this.state,
                    success: false,
                    loading: true,
                }, this.state.callback);
        }
    };

    render() {
        const {loading, success} = this.state;
        const {classes} = this.props;
        const buttonClassname = classNames({
            [classes.buttonSuccess]: success,
        });

        return (
            <div className={classes.root}>
                <div className={classes.wrapper}>
                    <Fab color="secondary" className={buttonClassname}
                         onClick={this.handleButtonClick}
                         disabled={loading}>
                        {this.state.normal_icon}
                    </Fab>
                    {loading && <CircularProgress size={68}
                                                  className={classes.fabProgress}/>}
                </div>
            </div>
        );
    }
}

LoadingIcon.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(LoadingIcon);