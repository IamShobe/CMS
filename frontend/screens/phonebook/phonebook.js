import React from "react";
import {List, AutoSizer} from "react-virtualized";
// import {ScrollBox, ScrollAxes, FastTrack} from 'react-scroll-box';
import Scrollbar from 'react-smooth-scrollbar';
import "./phonebook.scss";

export default class Phonebook extends React.Component {
    renderRow = ({index, isScrolling, key, style}) => {
        let numbers = this.props.book[index].numbers;
        let number = (numbers !== null) ? numbers[0] : "undefined";

        let image_src =
            (this.props.book[index].photo) ?
                `data:image/jpg;base64, ${this.props.book[index].photo}` :
                "/static/no-pic.png";
        let image = <img src={image_src}/>;

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

    renderList() {
        let to_ret = [];
        for (let index in this.props.book) {
            to_ret.push(this.renderRow({index: index, key: index}))
        }
        return to_ret;
    }


    handleScroll = (status, target) => {
        // const {scrollTop, scrollLeft} = target;
        this.list.Grid.handleScrollEvent({scrollTop:target.offset.y, scrollLeft: target.offset.x});

    };

    render() {
        return (
            <div className="container ">

                {/*{this.renderList()}*/}
                <AutoSizer>
                    {
                        ({width, height}) => {
                            return <Scrollbar damping={0.02}
                                              style={{
                                                  width: width,
                                                  height: height
                                              }}
                                              ref={node => this.scroll = node}
                                              onScroll={this.handleScroll.bind(this)}>
                                <List
                                    className={"contacts"}
                                    rowCount={this.props.book.length}
                                    width={width}
                                    height={height}
                                    rowHeight={100}
                                    rowRenderer={this.renderRow}
                                    ref={instance => (this.list = instance)}
                                    style={{
                                        overflowX: false,
                                        overflowY: false
                                    }}/>
                            </Scrollbar>
                        }
                    }
                </AutoSizer>

                {/*<PerfectScrollbar className="contacts">*/}


                {/*</PerfectScrollbar>*/}
            </div>
        );
    }
}