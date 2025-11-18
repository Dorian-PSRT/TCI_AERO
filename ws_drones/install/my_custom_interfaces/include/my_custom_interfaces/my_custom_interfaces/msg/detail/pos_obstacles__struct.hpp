// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_custom_interfaces:msg/PosObstacles.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_custom_interfaces/msg/pos_obstacles.hpp"


#ifndef MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_HPP_
#define MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'fixes'
// Member 'flotants'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__my_custom_interfaces__msg__PosObstacles __attribute__((deprecated))
#else
# define DEPRECATED__my_custom_interfaces__msg__PosObstacles __declspec(deprecated)
#endif

namespace my_custom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PosObstacles_
{
  using Type = PosObstacles_<ContainerAllocator>;

  explicit PosObstacles_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit PosObstacles_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _fixes_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _fixes_type fixes;
  using _flotants_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _flotants_type flotants;

  // setters for named parameter idiom
  Type & set__fixes(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->fixes = _arg;
    return *this;
  }
  Type & set__flotants(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->flotants = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_custom_interfaces__msg__PosObstacles
    std::shared_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_custom_interfaces__msg__PosObstacles
    std::shared_ptr<my_custom_interfaces::msg::PosObstacles_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PosObstacles_ & other) const
  {
    if (this->fixes != other.fixes) {
      return false;
    }
    if (this->flotants != other.flotants) {
      return false;
    }
    return true;
  }
  bool operator!=(const PosObstacles_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PosObstacles_

// alias to use template instance with default allocator
using PosObstacles =
  my_custom_interfaces::msg::PosObstacles_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_custom_interfaces

#endif  // MY_CUSTOM_INTERFACES__MSG__DETAIL__POS_OBSTACLES__STRUCT_HPP_
