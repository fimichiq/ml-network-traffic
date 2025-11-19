import type { Route } from "./+types/home";
import {Link} from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return (
      <>
        <h1>What is it?</h1>
        <p>Application allows to train, store and use machine learning models trained to classify network traffic as
        malicious or belonging to normal users. To make it work flawlessly, it is recommended to also use built-in
        PCAP to Netflow converter, since pretrained models are created with usage of CICFlowMeter. If you have new data
        it is also possible to train models with new types of malicious traffic.</p>
        <h2>How to use it?</h2>
        <h3>Classifying a network traffic</h3>
        <ul>
          <li>1. Capture a PCAP file</li>
          <li>2. Convert it to netflow format</li>
          <li>3. Choose a model and start</li>
        </ul>
        <h3>Training new/existing model</h3>
        <ul>
          <li>1. Create/find labeled netflow with specified format</li>
          <li>
            2. Go to <Link to="/train-models" style={{ color: 'lightblue', textDecoration: 'underline' }}>Train Model</Link> and start process
          </li>
        </ul>
      </>
  );
}
