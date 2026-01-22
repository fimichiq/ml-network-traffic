import type { Route } from "./+types/home";
import { Link } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "NetFlower - Network Traffic Classification" },
    { name: "description", content: "Classify network traffic using machine learning models" },
  ];
}

export default function Home() {
  return (
      <>
        <h1>What is it?</h1>
        <p>NetFlower is an application for classifying network traffic using machine learning models.
        It can detect malicious traffic and distinguish it from normal user activity. The application
        uses pretrained models based on CICFlowMeter features and includes a built-in PCAP to Netflow
        converter for seamless integration.</p>

        <h2>How to use it?</h2>

        <h3>1. Convert PCAP to Netflow</h3>
        <p>If you have a PCAP file, first convert it to netflow format using CICFlowMeter:</p>
        <ul>
          <li>Go to <Link to="/convert-pcap" style={{ color: 'lightblue', textDecoration: 'underline' }}>Convert PCAP</Link></li>
          <li>Upload your PCAP file</li>
          <li>Wait for conversion to complete</li>
        </ul>

        <h3>2. Classify Network Traffic</h3>
        <p>Use pretrained models to classify your network flows:</p>
        <ul>
          <li>Go to <Link to="/classify-traffic" style={{ color: 'lightblue', textDecoration: 'underline' }}>Classify Traffic</Link></li>
          <li>Select a model (binary for BENIGN/ATTACK or multi-class for specific attack types)</li>
          <li>Select a netflow CSV file</li>
          <li>Click Classify and download results as CSV</li>
        </ul>

        <h3>Available Models</h3>
        <ul>
          <li><strong>Binary models</strong> - classify traffic as BENIGN or ATTACK</li>
          <li><strong>Multi-class models</strong> - identify specific attack types (DoS, DDoS, PortScan, Brute Force, etc.)</li>
        </ul>
      </>
  );
}
