import React from 'react';
import Button from '@material-ui/core/Button/index';
import Dialog from '@material-ui/core/Dialog/index';
import DialogActions from '@material-ui/core/DialogActions/index';
import DialogContent from '@material-ui/core/DialogContent/index';
import DialogContentText from '@material-ui/core/DialogContentText/index';
import DialogTitle from '@material-ui/core/DialogTitle/index';
import Slide from '@material-ui/core/Slide/index';

function Transition(props) {
  return <Slide direction="up" {...props} />;
}

class AlertDialogSlide extends React.Component {
  state = {
    open: false,
    msg: "",
    title: ""
  };

  openWithMessage(title, msg, callback=undefined) {
    this.setState({
      ...this.state,
      open: true,
      title: title,
      msg: msg,
      callback: callback
    })
  }

  handleClose = () => {
    this.setState({ open: false });
  };

  handleAccept = () => {
    if (this.state.callback) {
      this.state.callback(true);
    }
    this.handleClose();
  };

  handleReject = () => {
    if (this.state.callback) {
      this.state.callback(false);
    }
    this.handleClose();
  };

  render() {
    return (
      <div>
        {/*<Button variant="outlined" color="primary" onClick={this.handleClickOpen}>*/}
        {/*  Slide in alert dialog*/}
        {/*</Button>*/}
        <Dialog
          open={this.state.open}
          TransitionComponent={Transition}
          keepMounted
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-slide-title"
          aria-describedby="alert-dialog-slide-description"
        >
          <DialogTitle id="alert-dialog-slide-title">
            {this.state.title}
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-slide-description"
            style={{ whiteSpace: "pre"}}>
              {this.state.msg}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleReject} color="primary">
              Reject
            </Button>
            <Button onClick={this.handleAccept} color="primary">
              Accept
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default AlertDialogSlide;