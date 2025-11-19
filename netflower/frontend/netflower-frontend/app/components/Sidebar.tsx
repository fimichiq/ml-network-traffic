import { useState } from "react";
import { Menu } from "lucide-react";
import { Link } from "react-router";

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`h-screen bg-gray-900 text-white p-4 transition-all duration-300 ${collapsed ? "w-16" : "w-64"}`}
    >
      <button
        className="mb-4 p-2 rounded bg-gray-700 hover:bg-gray-600"
        onClick={() => setCollapsed(!collapsed)}
      >
        <Menu size={24} />
      </button>
      <nav
        className={`transition-opacity duration-300 ${collapsed ? "opacity-0 invisible" : "opacity-100 visible"}`}
      >
        <ul>
          <li className="p-2 hover:bg-gray-700 rounded whitespace-nowrap">
            <Link to="/" className="block w-full h-full p-2">
              Home
            </Link>
          </li>
          <li className="p-2 hover:bg-gray-700 rounded whitespace-nowrap">
            <Link to="/convert-pcap" className="block w-full h-full p-2">
              Convert PCAP
            </Link>
          </li>
          <li className="p-2 hover:bg-gray-700 rounded whitespace-nowrap">
            <Link to="/train-models" className="block w-full h-full p-2">
              Train Model
            </Link>
          </li>
          <li className="p-2 hover:bg-gray-700 rounded whitespace-nowrap">
            <Link to="/classify-traffic" className="block w-full h-full p-2">
              Classify Traffic
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}