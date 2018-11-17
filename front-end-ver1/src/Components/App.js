import React, { Component, Fragment } from "react";
import { Header, Footer } from "./Layouts";
import { coins } from "../store.js";
export default class extends Component {
  states = {};
  render() {
    return (
      <Fragment>
        <Header />
        <Footer />
      </Fragment>
    );
  }
}
