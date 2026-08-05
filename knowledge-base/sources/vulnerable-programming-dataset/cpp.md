# Vulnerable Code Samples: C++

Secure-code-review training examples (60 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Use After Free

- **Language**: C++
- **Vulnerability**: Use After Free
- **Description**: Accessing memory after it has been freed.

```
#include <cstdlib>
void use_after_free() {
    int *ptr = new int(10);
    delete ptr;
    *ptr = 20;
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Use_After_Free
- CWE-416: https://cwe.mitre.org/data/definitions/416.html

## Sample 2 — Integer Overflow

- **Language**: C++
- **Vulnerability**: Integer Overflow
- **Description**: Not checking for integer overflow in arithmetic operations.

```
#include <cstdint>
int add(int a, int b) {
    return a + b;
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Integer_Overflow
- CWE-190: https://cwe.mitre.org/data/definitions/190.html

## Sample 3 — Null Pointer Dereference

- **Language**: C++
- **Vulnerability**: Null Pointer Dereference
- **Description**: Dereferencing a pointer without checking for null.

```
#include <iostream>
void process(int *ptr) {
    std::cout << *ptr;
}
```

**References**:
- CWE-476: https://cwe.mitre.org/data/definitions/476.html

## Sample 4 — Race Condition

- **Language**: C++
- **Vulnerability**: Race Condition
- **Description**: Accessing shared resource without synchronization.

```
#include <thread>
int counter = 0;
void increment() {
    for (int i = 0; i < 1000; i++) counter++;
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 5 — Buffer Overflow

- **Language**: C++
- **Vulnerability**: Buffer Overflow
- **Description**: Using gets() for unbounded input.

```
#include <cstdio>
void read_input() {
    char buffer[10];
    gets(buffer);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Buffer_Overflow
- CWE-120: https://cwe.mitre.org/data/definitions/120.html

## Sample 6 — Memory Leak

- **Language**: C++
- **Vulnerability**: Memory Leak
- **Description**: Failing to free allocated memory.

```
#include <cstdlib>
void allocate() {
    int *ptr = new int[100];
    // No delete
}
```

**References**:
- CWE-401: https://cwe.mitre.org/data/definitions/401.html

## Sample 7 — Format String Vulnerability

- **Language**: C++
- **Vulnerability**: Format String Vulnerability
- **Description**: Using user input in format string.

```
#include <cstdio>
void print_data(char *input) {
    printf(input);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Format_string_attack
- CWE-134: https://cwe.mitre.org/data/definitions/134.html

## Sample 8 — Uninitialized Variable

- **Language**: C++
- **Vulnerability**: Uninitialized Variable
- **Description**: Using a variable before initialization.

```
#include <iostream>
void print_value() {
    int x;
    std::cout << x;
}
```

**References**:
- CWE-457: https://cwe.mitre.org/data/definitions/457.html

## Sample 9 — Double Free

- **Language**: C++
- **Vulnerability**: Double Free
- **Description**: Freeing a pointer twice.

```
#include <cstdlib>
void double_free() {
    int *ptr = new int;
    delete ptr;
    delete ptr;
}
```

**References**:
- CWE-415: https://cwe.mitre.org/data/definitions/415.html

## Sample 10 — Out-of-Bounds Access

- **Language**: C++
- **Vulnerability**: Out-of-Bounds Access
- **Description**: Accessing array beyond its bounds.

```
#include <vector>
void access_array() {
    std::vector<int> vec(5);
    vec[10] = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 11 — Insecure Temporary File

- **Language**: C++
- **Vulnerability**: Insecure Temporary File
- **Description**: Creating temporary files in predictable locations.

```
#include <cstdio>
void create_temp_file() {
    FILE *f = fopen("/tmp/tempfile", "w");
    fclose(f);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-377: https://cwe.mitre.org/data/definitions/377.html

## Sample 12 — Use After Free

- **Language**: C++
- **Vulnerability**: Use After Free
- **Description**: Accessing memory after it has been freed.

```
#include <cstdlib>
void use_after_free() {
    int *ptr = new int(10);
    delete ptr;
    *ptr = 20;
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Use_After_Free
- CWE-416: https://cwe.mitre.org/data/definitions/416.html

## Sample 13 — Integer Overflow

- **Language**: C++
- **Vulnerability**: Integer Overflow
- **Description**: Not checking for integer overflow in arithmetic operations.

```
#include <cstdint>
int add(int a, int b) {
    return a + b;
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Integer_Overflow
- CWE-190: https://cwe.mitre.org/data/definitions/190.html

## Sample 14 — Null Pointer Dereference

- **Language**: C++
- **Vulnerability**: Null Pointer Dereference
- **Description**: Dereferencing a pointer without checking for null.

```
#include <iostream>
void process(int *ptr) {
    std::cout << *ptr;
}
```

**References**:
- CWE-476: https://cwe.mitre.org/data/definitions/476.html

## Sample 15 — Race Condition

- **Language**: C++
- **Vulnerability**: Race Condition
- **Description**: Accessing shared resource without synchronization.

```
#include <thread>
int counter = 0;
void increment() {
    for (int i = 0; i < 1000; i++) counter++;
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 16 — Buffer Overflow

- **Language**: C++
- **Vulnerability**: Buffer Overflow
- **Description**: Using gets() for unbounded input.

```
#include <cstdio>
void read_input() {
    char buffer[10];
    gets(buffer);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Buffer_Overflow
- CWE-120: https://cwe.mitre.org/data/definitions/120.html

## Sample 17 — Memory Leak

- **Language**: C++
- **Vulnerability**: Memory Leak
- **Description**: Failing to free allocated memory.

```
#include <cstdlib>
void allocate() {
    int *ptr = new int[100];
    // No delete
}
```

**References**:
- CWE-401: https://cwe.mitre.org/data/definitions/401.html

## Sample 18 — Format String Vulnerability

- **Language**: C++
- **Vulnerability**: Format String Vulnerability
- **Description**: Using user input in format string.

```
#include <cstdio>
void print_data(char *input) {
    printf(input);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Format_string_attack
- CWE-134: https://cwe.mitre.org/data/definitions/134.html

## Sample 19 — Uninitialized Variable

- **Language**: C++
- **Vulnerability**: Uninitialized Variable
- **Description**: Using a variable before initialization.

```
#include <iostream>
void print_value() {
    int x;
    std::cout << x;
}
```

**References**:
- CWE-457: https://cwe.mitre.org/data/definitions/457.html

## Sample 20 — Double Free

- **Language**: C++
- **Vulnerability**: Double Free
- **Description**: Freeing a pointer twice.

```
#include <cstdlib>
void double_free() {
    int *ptr = new int;
    delete ptr;
    delete ptr;
}
```

**References**:
- CWE-415: https://cwe.mitre.org/data/definitions/415.html

## Sample 21 — Out-of-Bounds Access

- **Language**: C++
- **Vulnerability**: Out-of-Bounds Access
- **Description**: Accessing array beyond its bounds.

```
#include <vector>
void access_array() {
    std::vector<int> vec(5);
    vec[10] = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 22 — Insecure Temporary File

- **Language**: C++
- **Vulnerability**: Insecure Temporary File
- **Description**: Creating temporary files in predictable locations.

```
#include <cstdio>
void create_temp_file() {
    FILE *f = fopen("/tmp/tempfile", "w");
    fclose(f);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-377: https://cwe.mitre.org/data/definitions/377.html

## Sample 23 — Insecure Signal Handling

- **Language**: C++
- **Vulnerability**: Insecure Signal Handling
- **Description**: Improper handling of signals leading to undefined behavior.

```
#include <signal.h>
void handler(int sig) {
    // Unsafe operations
}
void setup() {
    signal(SIGINT, handler);
}
```

**References**:
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 24 — Insecure Exception Handling

- **Language**: C++
- **Vulnerability**: Insecure Exception Handling
- **Description**: Catching all exceptions without specific handling.

```
#include <exception>
void process() {
    try {
        // Code
    } catch (...) {
        // Ignore all exceptions
    }
}
```

**References**:
- CWE-396: https://cwe.mitre.org/data/definitions/396.html

## Sample 25 — Insecure Shared Memory

- **Language**: C++
- **Vulnerability**: Insecure Shared Memory
- **Description**: Using shared memory without access controls.

```
#include <sys/shm.h>
void* create_shared_memory() {
    int shmid = shmget(IPC_PRIVATE, 1024, 0666);
    return shmat(shmid, NULL, 0);
}
```

**References**:
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 26 — Insecure Shared Library Loading

- **Language**: C++
- **Vulnerability**: Insecure Shared Library Loading
- **Description**: Loading libraries from untrusted paths, risking DLL injection.

```
#include <dlfcn.h>
void load_library(const char* path) {
    void* handle = dlopen(path, RTLD_LAZY);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/
- CWE-426: https://cwe.mitre.org/data/definitions/426.html

## Sample 27 — Insecure Memory Mapping

- **Language**: C++
- **Vulnerability**: Insecure Memory Mapping
- **Description**: Using mmap with unprotected memory regions.

```
#include <sys/mman.h>
void* map_memory(size_t size) {
    return mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, -1, 0);
}
```

**References**:
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 28 — Insecure Atomic Operation

- **Language**: C++
- **Vulnerability**: Insecure Atomic Operation
- **Description**: Using non-atomic operations in concurrent code.

```
#include <thread>
int counter = 0;
void increment() {
    counter++;
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 29 — Insecure Pointer Arithmetic

- **Language**: C++
- **Vulnerability**: Insecure Pointer Arithmetic
- **Description**: Performing pointer arithmetic without bounds checking.

```
#include <iostream>
void process(int* ptr, int offset) {
    *(ptr + offset) = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 30 — Insecure Thread Termination

- **Language**: C++
- **Vulnerability**: Insecure Thread Termination
- **Description**: Terminating threads without cleanup.

```
#include <thread>
void run() {
    std::thread t([](){});
    // No join or detach
}
```

**References**:
- CWE-404: https://cwe.mitre.org/data/definitions/404.html

## Sample 31 — Insecure Dynamic Memory Allocation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Memory Allocation
- **Description**: Allocating memory without checking size constraints.

```
#include <cstdlib>
void allocate(size_t size) {
    char* buf = (char*)malloc(size);
    strcpy(buf, "data");
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html

## Sample 32 — Insecure Resource Cleanup

- **Language**: C++
- **Vulnerability**: Insecure Resource Cleanup
- **Description**: Failing to release resources properly.

```
#include <fstream>
void process() {
    std::ofstream file("data.txt");
    // No file.close()
}
```

**References**:
- CWE-404: https://cwe.mitre.org/data/definitions/404.html

## Sample 33 — Insecure Dynamic Cast

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Cast
- **Description**: Using dynamic_cast without type safety checks.

```
#include <typeinfo>
class Base {};
class Derived : public Base {};
void cast(Base* b) {
    Derived* d = dynamic_cast<Derived*>(b);
    d->method();
}
```

**References**:
- CWE-704: https://cwe.mitre.org/data/definitions/704.html

## Sample 34 — Insecure Dynamic Type Creation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Type Creation
- **Description**: Creating types dynamically without validation.

```
#include <typeinfo>
void create_type(const char* name) {
    typeid(name).name();
}
```

**References**:
- CWE-704: https://cwe.mitre.org/data/definitions/704.html

## Sample 35 — Insecure Dynamic Function Pointer

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Function Pointer
- **Description**: Using function pointers with unvalidated input.

```
#include <functional>
void call(void (*func)()) {
    func();
}
```

**References**:
- CWE-822: https://cwe.mitre.org/data/definitions/822.html

## Sample 36 — Insecure Dynamic Object Creation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Object Creation
- **Description**: Creating objects dynamically without type safety.

```
#include <memory>
void create(void* data) {
    std::shared_ptr<void> ptr(data);
}
```

**References**:
- CWE-704: https://cwe.mitre.org/data/definitions/704.html

## Sample 37 — Insecure Dynamic Memory Reallocation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Memory Reallocation
- **Description**: Reallocating memory without validation.

```
#include <cstdlib>
void reallocate(void* ptr, size_t size) {
    realloc(ptr, size);
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html

## Sample 38 — Insecure Dynamic Buffer Access

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Buffer Access
- **Description**: Accessing buffers dynamically without bounds checking.

```
#include <vector>
void access_buffer(std::vector<int>& vec, int index) {
    vec[index] = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 39 — Insecure Dynamic Signal Handler

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Signal Handler
- **Description**: Registering signal handlers without validation.

```
#include <signal.h>
void register_handler(void (*handler)(int)) {
    signal(SIGINT, handler);
}
```

**References**:
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 40 — Insecure Dynamic Exception Handling

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Exception Handling
- **Description**: Catching exceptions without validating types.

```
#include <exception>
void handle() {
    try { throw 42; } catch (...) { std::cout << "Caught"; }
}
```

**References**:
- CWE-703: https://cwe.mitre.org/data/definitions/703.html

## Sample 41 — Insecure Dynamic Resource Allocation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Resource Allocation
- **Description**: Allocating resources dynamically without limits.

```
#include <vector>
void allocate(size_t size) {
    std::vector<char> vec(size);
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html

## Sample 42 — Insecure Dynamic Thread Pool

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Thread Pool
- **Description**: Creating thread pools with unbounded sizes.

```
#include <thread>
void create_pool(int size) {
    std::vector<std::thread> pool(size);
}
```

**References**:
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 43 — Insecure Dynamic Mutex Creation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Mutex Creation
- **Description**: Creating mutexes without initialization checks.

```
#include <mutex>
void create_mutex() {
    std::mutex mtx;
    mtx.lock();
}
```

**References**:
- CWE-667: https://cwe.mitre.org/data/definitions/667.html

## Sample 44 — Insecure Dynamic Iterator Access

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Iterator Access
- **Description**: Accessing iterators without bounds checking.

```
#include <vector>
void access(std::vector<int>& vec, int pos) {
    auto it = vec.begin() + pos;
    *it = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 45 — Insecure Dynamic Condition Variable

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Condition Variable
- **Description**: Using condition variables without proper initialization.

```
#include <condition_variable>
void wait() {
    std::condition_variable cv;
    std::mutex mtx;
    cv.wait(mtx);
}
```

**References**:
- CWE-667: https://cwe.mitre.org/data/definitions/667.html

## Sample 46 — Insecure Dynamic Shared Memory

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Shared Memory
- **Description**: Using shared memory without access controls.

```
#include <sys/shm.h>
void create_shm(int size) {
    shmget(IPC_PRIVATE, size, IPC_CREAT | 0666);
}
```

**References**:
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 47 — Insecure Dynamic Semaphore Creation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Semaphore Creation
- **Description**: Creating semaphores without initialization checks.

```
#include <semaphore.h>
void create_sem() {
    sem_t sem;
    sem_post(&sem);
}
```

**References**:
- CWE-667: https://cwe.mitre.org/data/definitions/667.html

## Sample 48 — Insecure Dynamic Weak Pointer

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Weak Pointer
- **Description**: Using weak pointers without validation.

```
#include <memory>
void access(std::weak_ptr<int> wp) {
    if (auto sp = wp.lock()) { *sp = 42; }
}
```

**References**:
- CWE-824: https://cwe.mitre.org/data/definitions/824.html

## Sample 49 — Insecure Dynamic Memory Alignment

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Memory Alignment
- **Description**: Aligning memory without validation.

```
#include <memory>
void align_memory(size_t alignment) {
    std::align(alignment, sizeof(int), ptr, space);
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html

## Sample 50 — Insecure Dynamic Atomic Access

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Atomic Access
- **Description**: Accessing atomic variables without proper synchronization.

```
#include <atomic>
void access(std::atomic<int>& val) {
    val = 42;
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 51 — Insecure Dynamic Reference Counting

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Reference Counting
- **Description**: Manipulating reference counts without validation.

```
#include <memory>
void modify_ref(std::shared_ptr<int> sp) {
    sp.use_count();
    *sp = 42;
}
```

**References**:
- CWE-672: https://cwe.mitre.org/data/definitions/672.html

## Sample 52 — Insecure Dynamic Volatile Access

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Volatile Access
- **Description**: Accessing volatile variables without synchronization.

```
#include <atomic>
void access(volatile int& val) {
    val = 42;
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 53 — Insecure Dynamic Function Pointer

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Function Pointer
- **Description**: Using function pointers without validation.

```
#include <functional>
void call(void (*func)()) {
    func();
}
```

**References**:
- CWE-822: https://cwe.mitre.org/data/definitions/822.html

## Sample 54 — Insecure Dynamic Array Indexing

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Array Indexing
- **Description**: Indexing arrays without bounds checking.

```
#include <array>
void access(std::array<int, 10>& arr, int index) {
    arr[index] = 42;
}
```

**References**:
- CWE-119: https://cwe.mitre.org/data/definitions/119.html

## Sample 55 — Insecure Dynamic Virtual Function

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Virtual Function
- **Description**: Calling virtual functions without validation.

```
#include <functional>
struct Base {
    virtual void call() {}
};
void invoke(Base* obj) {
    obj->call();
}
```

**References**:
- CWE-822: https://cwe.mitre.org/data/definitions/822.html

## Sample 56 — Insecure Dynamic Stack Allocation

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Stack Allocation
- **Description**: Allocating stack memory without bounds checking.

```
#include <alloca.h>
void allocate(size_t size) {
    void* ptr = alloca(size);
    memset(ptr, 0, size);
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html

## Sample 57 — Insecure Dynamic Lambda Capture

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Lambda Capture
- **Description**: Capturing variables in lambdas without validation.

```
#include <functional>
void capture(int* ptr) {
    auto lambda = [ptr]() { *ptr = 42; };
    lambda();
}
```

**References**:
- CWE-822: https://cwe.mitre.org/data/definitions/822.html

## Sample 58 — Insecure Dynamic Type Casting

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Type Casting
- **Description**: Casting types dynamically without validation.

```
#include <typeinfo>
void cast(void* ptr, const std::type_info& type) {
    typeid(*ptr) == type;
}
```

**References**:
- CWE-704: https://cwe.mitre.org/data/definitions/704.html

## Sample 59 — Insecure Dynamic Exception Specification

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Exception Specification
- **Description**: Using exception specifications without validation.

```
#include <stdexcept>
void throwException() throw(int) {
    throw 42;
}
```

**References**:
- CWE-703: https://cwe.mitre.org/data/definitions/703.html

## Sample 60 — Insecure Dynamic Allocator

- **Language**: C++
- **Vulnerability**: Insecure Dynamic Allocator
- **Description**: Using custom allocators without validation.

```
#include <memory>
void allocate(std::allocator<char>& alloc, size_t size) {
    alloc.allocate(size);
}
```

**References**:
- CWE-789: https://cwe.mitre.org/data/definitions/789.html
