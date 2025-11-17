// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_custom_interfaces:srv/Position3D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/srv/position3_d.hpp"


#ifndef MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__TRAITS_HPP_
#define MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "my_custom_interfaces/srv/detail/position3_d__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'point'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace my_custom_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Position3D_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: point
  {
    out << "point: ";
    to_flow_style_yaml(msg.point, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Position3D_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point:\n";
    to_block_style_yaml(msg.point, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Position3D_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace my_custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_interfaces::srv::Position3D_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_interfaces::srv::Position3D_Request & msg)
{
  return my_custom_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_interfaces::srv::Position3D_Request>()
{
  return "my_custom_interfaces::srv::Position3D_Request";
}

template<>
inline const char * name<my_custom_interfaces::srv::Position3D_Request>()
{
  return "my_custom_interfaces/srv/Position3D_Request";
}

template<>
struct has_fixed_size<my_custom_interfaces::srv::Position3D_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value> {};

template<>
struct has_bounded_size<my_custom_interfaces::srv::Position3D_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value> {};

template<>
struct is_message<my_custom_interfaces::srv::Position3D_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace my_custom_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Position3D_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Position3D_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Position3D_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace my_custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_interfaces::srv::Position3D_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_interfaces::srv::Position3D_Response & msg)
{
  return my_custom_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_interfaces::srv::Position3D_Response>()
{
  return "my_custom_interfaces::srv::Position3D_Response";
}

template<>
inline const char * name<my_custom_interfaces::srv::Position3D_Response>()
{
  return "my_custom_interfaces/srv/Position3D_Response";
}

template<>
struct has_fixed_size<my_custom_interfaces::srv::Position3D_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<my_custom_interfaces::srv::Position3D_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<my_custom_interfaces::srv::Position3D_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace my_custom_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Position3D_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Position3D_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Position3D_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace my_custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_interfaces::srv::Position3D_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_interfaces::srv::Position3D_Event & msg)
{
  return my_custom_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_interfaces::srv::Position3D_Event>()
{
  return "my_custom_interfaces::srv::Position3D_Event";
}

template<>
inline const char * name<my_custom_interfaces::srv::Position3D_Event>()
{
  return "my_custom_interfaces/srv/Position3D_Event";
}

template<>
struct has_fixed_size<my_custom_interfaces::srv::Position3D_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_custom_interfaces::srv::Position3D_Event>
  : std::integral_constant<bool, has_bounded_size<my_custom_interfaces::srv::Position3D_Request>::value && has_bounded_size<my_custom_interfaces::srv::Position3D_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<my_custom_interfaces::srv::Position3D_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<my_custom_interfaces::srv::Position3D>()
{
  return "my_custom_interfaces::srv::Position3D";
}

template<>
inline const char * name<my_custom_interfaces::srv::Position3D>()
{
  return "my_custom_interfaces/srv/Position3D";
}

template<>
struct has_fixed_size<my_custom_interfaces::srv::Position3D>
  : std::integral_constant<
    bool,
    has_fixed_size<my_custom_interfaces::srv::Position3D_Request>::value &&
    has_fixed_size<my_custom_interfaces::srv::Position3D_Response>::value
  >
{
};

template<>
struct has_bounded_size<my_custom_interfaces::srv::Position3D>
  : std::integral_constant<
    bool,
    has_bounded_size<my_custom_interfaces::srv::Position3D_Request>::value &&
    has_bounded_size<my_custom_interfaces::srv::Position3D_Response>::value
  >
{
};

template<>
struct is_service<my_custom_interfaces::srv::Position3D>
  : std::true_type
{
};

template<>
struct is_service_request<my_custom_interfaces::srv::Position3D_Request>
  : std::true_type
{
};

template<>
struct is_service_response<my_custom_interfaces::srv::Position3D_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__TRAITS_HPP_
