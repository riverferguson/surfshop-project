import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Nav from "./Nav";
import ProductPage from "./ProductPage";
import Signin from "./Signin";
import Signup from "./Signup";

function App() {
  const [products, setProducts] = useState([]);
  const [user, setUser] = useState(null);
  const onSign = (user) => setUser(user);

  useEffect(() => {
    fetch("/products")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
      });
  }, []);

  // useEffect(() => {
  //   fetch("/check_session").then((r) => {
  //     if (r.ok) {
  //       r.json().then((user) => setUser(user));
  //       // setUser(current => !current)
  //     } else {
  //       setUser(null)
  //     }
  //   });
  // }, []);

  return (
    <main>
      <Nav user={user} />
      <Switch>
        <Route>
          <ProductPage products={products} />
        </Route>
        <Route exact path="/signin">
          <Signin onSign={onSign} />
        </Route>
        <Route exact path="/signup">
          <Signup onSign={onSign} />
        </Route>
      </Switch>
    </main>
  );
}

export default App;
