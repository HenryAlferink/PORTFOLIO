import React, { Component } from "react";
// added the following line
import PropTypes from "prop-types";

// class based component
class Navbar extends Component {
  // default properties if you didn't specify any in the Navbar element in App.js
  static defaultProps = {
    title: "Github Finder",
    icon: "fab fa-github",
  };

  // this specifies what the input types must be for the element props.
  // if the wrong type is given, an error will be shown (though the page
  // will still render.)
  static propTypes = {
    title: PropTypes.string.isRequired,
    icon: PropTypes.string.isRequired,
  };

  render() {
    return (
      <nav className='navbar bg-primary'>
        <h1>
          <i className={this.props.icon} /> {this.props.title}
        </h1>
      </nav>
    );
  }
}

export default Navbar;
