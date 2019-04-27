const ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;
const {render} = ReactDOM;
const {Route, Router, hashHistory} = ReactRouter;

const transitionClassName = "transition-group";
const pageTransitionName = "page";
const repoTransitionName = "repo";
const transitionDuration = 300;
const transitionEnterTimeout = 2 * transitionDuration;

render(
  <Router history={hashHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={Home}/>
      <Route path="/repos" component={Repos}>
        <Route path="/repos/:userName/:repoName" component={Repo}/>
      </Route>
      <Route path="/about" component={About}/>
    </Route>
  </Router>,
  document.getElementById('app')
);

function App(props) {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-heading">
          <NavLink to="/">React Router V2 with ReactCSSTransitionGroup</NavLink>
        </h1>
        <nav>
          <ul className="App-navList">
            <li><NavLink to="/" onlyActiveOnIndex={true}>Home</NavLink></li>
            <li><NavLink to="/about">About</NavLink></li>
            <li><NavLink to="/repos">Repos</NavLink></li>
          </ul>
        </nav>
      </header>
      <main className="App-body">
        <ReactCSSTransitionGroup
          component="div"
          className={transitionClassName}
          transitionName={pageTransitionName}
          transitionEnterTimeout={transitionEnterTimeout}
          transitionLeaveTimeout={transitionDuration}
        >
          {React.cloneElement(props.children, {
              key: getSubstringUntilNth(props.location.pathname, '/', 2)
          })}
        </ReactCSSTransitionGroup>
      </main>
    </div>
  );
}

function NavLink(props) {
  return <Link {...props} className="NavLink" activeClassName="active"/>;
}

function Home() {
  return (
    <div className="Home">
      <h2 className="Home-heading">Home</h2>
      <p>Welcome to the demo! Try navigating around.</p>
      <p>For React Router V4, <a href="https://codepen.io/tansongyang/pen/rzjJvj">see here</a>.</p>
    </div>
  );
}

function About() {
  return (
    <div className="About">
      <h2 className="About-heading">About</h2>
      <p className="About-body">I did this experiment to learn how to add CSS transitions between changes in routes. Look for <code>ReactCSSTransitionGroup</code> in the JS, then see the corresponding CSS.</p>
    </div>
  );
}

function Repos(props) {
  return (
    <div className="Repos">
        <nav className="Repos-nav">
          <h2 className="Repos-heading">Repos</h2>
          <ul>
            <li><NavLink to="/repos/facebook/react">react</NavLink></li>
            <li><NavLink to="/repos/reactjs/react-router">react-router</NavLink></li>
            <li><NavLink to="/repos/reactjs/react-router-tutorial">react-router-tutorial</NavLink></li>
          </ul>
        </nav>
        <ReactCSSTransitionGroup
          component="div"
          className={`${transitionClassName} Repos-repoContainer`}
          transitionName={repoTransitionName}
          transitionEnterTimeout={transitionEnterTimeout}
          transitionLeaveTimeout={transitionDuration}
        >
          {props.children ?
            React.cloneElement(props.children, {
              key: props.location.pathname
            }) :
            null}
        </ReactCSSTransitionGroup>
    </div>
  );
}

function Repo(props) {
  const {userName, repoName} = props.params;
  return (
    <div className="Repo">
      <h3 className="Repo-heading">{repoName}</h3>
      <div className="Repo-body">
        <p>
          <a href={`https://github.com/${userName}/${repoName}`}>More information</a> about this repo.
        </p>
      </div>
    </div>
  );
}

function getSubstringUntilNth(str, pattern, n) {
  return  str.split(pattern, n).join(pattern);
}