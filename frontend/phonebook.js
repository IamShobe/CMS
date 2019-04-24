import React from "react";
import { List, AutoSizer } from "react-virtualized";


import "./phonebook.scss";

export class Phonebook extends React.Component {
  renderRow = ({ index, isScrolling, key, style}) => {
    let numbers = this.props.book[index].numbers;
    let number = (numbers !== null)? numbers[0] : "undefined";

    let image_src =
        (this.props.book[index].photo)?
            `data:image/jpg;base64, ${this.props.book[index].photo}`:
            "/static/no-pic.png";
    let image = <img src={image_src} />;

    return (
      <div className="contact" key={key} style={style}>
        <div className="picture">{image}</div>
        <div className="details">
          <div className="name">{this.props.book[index].name}</div>
          <div className="number">{number}</div>
        </div>
      </div>
    )
  };

  componentWillReceiveProps(nextProps, nextContext) {
    this.setState({...this.state})
  }

  render() {
    return (
      <AutoSizer>
      {
        ({ width, height }) => {
          return <List
            rowCount={this.props.book.length}
            width={width}
            height={height}
            rowHeight={100}
            rowRenderer={this.renderRow}
          />
        }
      }
      </AutoSizer>
    );
  }
}