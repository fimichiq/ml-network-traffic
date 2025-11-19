import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("train-models", "routes/train.tsx"),
    route("convert-pcap", "routes/convert.tsx"),
    route("classify-traffic", "routes/classify.tsx"),
] satisfies RouteConfig;
