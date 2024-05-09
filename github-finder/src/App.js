import "./App.css";

// added theses import lines
import React, { Component } from "react";
import Navbar from "./components/layout/Navbar";
import Users from "./components/Users/Users";

class App extends Component {
  render() {
    return (
      <div className='App'>
        {/*here we give the Navbar element the 'title' and 'icon' props*/}
        <Navbar title='Hello World' icon='fab fa-github' />
        <div className='container'>
          <Users />
        </div>
      </div>
    );
  }
}

// functional component
/*
function App() {
  return (
    <div className='App'>
      <h1>Hello World!</h1>
    </div>
  );
}
*/

// class-based component (as opposed to a functional component)
// class App extends Component {
//   classFunction = () => "Hello World!";

//   render() {
//     /*Lifecycle method. This one runs when the component is loaded.
//     render() is the only one (?) that is actually required, because
//     it renders the output.
//     */

//     const name = "Henry Alferink";
//     const loading = true;
//     const showName = true;

//     // use ternary operator instead of this...
//     // if(loading) {
//     //   return <h4>Loading...</h4>
//     // }

//     const foo = () => "Hello World...";

//     return (
//       // this is not HTML. It is JSX - Javascript Syntax Extension.
//       // You don't technically need to use JSX, but it'll save time.
//       <div className='App'>
//         {/*use className instead of class in JSX */}
//         {/* JSX must always have ONLY ONE parent element, ie. <div> */}
//         <h1>Hello {showName && name.toUpperCase() + "!"}</h1>

//         {/*ternary operator...*/}
//         {loading ? (
//           <h4>Loading...</h4>
//         ) : (
//           <h4>
//             {4 + 2}
//             {foo()}
//             {this.classFunction()}
//           </h4>
//         )}
//       </div>

//       // use <React.Fragment> instead of <div> if wanting to remove <div> altogether. eg.
//       /*
//       <React.Fragment className='App'>
//         <h1>Hello World!</h1>
//       </React.Fragment>
//       */
//     );

//     /*
//     // You can use straight Javascript instead of JSX (but why would you...):
//     return React.createElement(
//       'div',
//       { className: 'App' },
//       React.createElement('h1', null, 'Hello World!')
//     );
//     */
//   }
// }

export default App;
