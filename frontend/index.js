import axios from "axios";
import React from "react";
import ReactDOM from "react-dom";


import {Phonebook} from "./phonebook";

import "./style.scss";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            book: []
        };
    }
    componentDidMount() {
        axios.get('/static/phonebook.json')
                .then( (json) => {

                    // The data from the request is available in a .then block
                    // We return the result using resolve.
                    console.log(json.data);
                    this.setState({
                        ...this.state,
                        book: json.data
                    })
                });
    }

    render() {
        return (<Phonebook book={this.state.book}/>);
    }
}

ReactDOM.render(<App/>, document.getElementById("root"));