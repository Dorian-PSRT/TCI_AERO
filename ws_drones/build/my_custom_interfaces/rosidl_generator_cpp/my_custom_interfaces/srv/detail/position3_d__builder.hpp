// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_custom_interfaces:srv/Position3D.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/srv/position3_d.hpp"


#ifndef MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__BUILDER_HPP_
#define MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_custom_interfaces/srv/detail/position3_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_Position3D_Request_point
{
public:
  Init_Position3D_Request_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_custom_interfaces::srv::Position3D_Request point(::my_custom_interfaces::srv::Position3D_Request::_point_type arg)
  {
    msg_.point = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_interfaces::srv::Position3D_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_interfaces::srv::Position3D_Request>()
{
  return my_custom_interfaces::srv::builder::Init_Position3D_Request_point();
}

}  // namespace my_custom_interfaces


namespace my_custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_Position3D_Response_success
{
public:
  Init_Position3D_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_custom_interfaces::srv::Position3D_Response success(::my_custom_interfaces::srv::Position3D_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_interfaces::srv::Position3D_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_interfaces::srv::Position3D_Response>()
{
  return my_custom_interfaces::srv::builder::Init_Position3D_Response_success();
}

}  // namespace my_custom_interfaces


namespace my_custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_Position3D_Event_response
{
public:
  explicit Init_Position3D_Event_response(::my_custom_interfaces::srv::Position3D_Event & msg)
  : msg_(msg)
  {}
  ::my_custom_interfaces::srv::Position3D_Event response(::my_custom_interfaces::srv::Position3D_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_interfaces::srv::Position3D_Event msg_;
};

class Init_Position3D_Event_request
{
public:
  explicit Init_Position3D_Event_request(::my_custom_interfaces::srv::Position3D_Event & msg)
  : msg_(msg)
  {}
  Init_Position3D_Event_response request(::my_custom_interfaces::srv::Position3D_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Position3D_Event_response(msg_);
  }

private:
  ::my_custom_interfaces::srv::Position3D_Event msg_;
};

class Init_Position3D_Event_info
{
public:
  Init_Position3D_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Position3D_Event_request info(::my_custom_interfaces::srv::Position3D_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Position3D_Event_request(msg_);
  }

private:
  ::my_custom_interfaces::srv::Position3D_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_interfaces::srv::Position3D_Event>()
{
  return my_custom_interfaces::srv::builder::Init_Position3D_Event_info();
}

}  // namespace my_custom_interfaces

#endif  // MY_CUSTOM_INTERFACES__SRV__DETAIL__POSITION3_D__BUILDER_HPP_
