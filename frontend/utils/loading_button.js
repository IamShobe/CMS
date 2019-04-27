import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles/index';
import CircularProgress from '@material-ui/core/CircularProgress/index';
import green from '@material-ui/core/colors/green';
import Button from '@material-ui/core/Button/index';


const styles = theme => ({
  root: {
    display: 'flex',
    alignItems: 'center',
  },
  wrapper: {
    margin: theme.spacing.unit,
    position: 'relative',
  },
  buttonSuccess: {
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
  buttonProgress: {
    color: green[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
});

class LoadingButton extends React.Component {
  state = {
    loading: false,
    success: false,
  };

  constructor(props) {
    super(props);
    this.state = {
      ...this.state,
      callback: this.props.callback,
      title: this.props.title
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
    const { loading, success } = this.state;
    const { classes } = this.props;
    const buttonClassname = classNames({
      [classes.buttonSuccess]: success,
    });

    return (
      <div className={classes.root}>
        <div className={classes.wrapper}>
          <Button
            variant="contained"
            color="primary"
            className={buttonClassname}
            disabled={loading}
            onClick={this.handleButtonClick}
          >
            {this.state.title}
          </Button>
          {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
        </div>
      </div>
    );
  }
}

LoadingButton.propTypes = {
  classes: PropTypes.object.isRequired,
  title: PropTypes.string.isRequired,
};

export default withStyles(styles)(LoadingButton);