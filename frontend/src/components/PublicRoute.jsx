/* eslint-disable react/prop-types */
import { Navigate } from "react-router-dom";

const PublicRoute = ({ isAuthenticated, children }) => {
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default PublicRoute;
