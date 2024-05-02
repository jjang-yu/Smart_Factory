#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <cmath>
#include <map>
#include <chrono>
#include <thread>
#define M_PI           3.14159265358979323846  /* pi */
using namespace cv;
using namespace std;

QRCodeDetector qrDecoder = QRCodeDetector::QRCodeDetector();

class QRcode {
public:
    map<string, string> qr_decode(Mat& frame) {
        Mat dark_frame;
        convertScaleAbs(frame, dark_frame, 0.1, 0);
        map<string, string> QR;
        Mat bbox, rectifiedImage;

        std::string data = qrDecoder.detectAndDecode(frame, bbox, rectifiedImage);
        if (data.length() > 0)
        {
            cout << "Decoded Data : " << data << endl;

            rectifiedImage.convertTo(rectifiedImage, CV_8UC3);
            imshow("Rectified QRCode", rectifiedImage);
        }
        else
            cout << "QR Code not detected" << endl;
        return QR;
    }
};

class Shapes {
public:
    map<string, string> shapes_decode(Mat img) {
        string rec_detected = "";

        Mat hsv;
        cvtColor(img, hsv, COLOR_BGR2HSV);

        Scalar lower_red(170, 50, 50), upper_red(180, 255, 255);
        Scalar lower_yellow(15, 50, 50), upper_yellow(30, 255, 255);
        Scalar lower_green(35, 40, 0), upper_green(85, 255, 255);
        Scalar lower_blue(90, 100, 100), upper_blue(130, 255, 255); 
        Scalar lower_orange(0, 50, 50), upper_orange(30, 255, 255);

        Mat mask_red, mask_yellow, mask_green, mask_blue, mask_orange;
        inRange(hsv, lower_red, upper_red, mask_red);
        inRange(hsv, lower_yellow, upper_yellow, mask_yellow);
        inRange(hsv, lower_green, upper_green, mask_green);
        inRange(hsv, lower_blue, upper_blue, mask_blue);
        inRange(hsv, lower_orange, upper_orange, mask_orange);

        Mat mask = mask_green | mask_red | mask_yellow | mask_blue | mask_orange;

        Mat masked_image;
        bitwise_and(img, img, masked_image, mask);
        Mat dark_frame;
        convertScaleAbs(masked_image, dark_frame, 0.8, 2);
        Mat edge_img;
        Canny(dark_frame, edge_img, 100, 200);
        vector<vector<Point>> contours;
        findContours(edge_img, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);
        for (auto& contour : contours) {
            double epsilon = 0.02 * arcLength(contour, true);
            vector<Point> approx;
            approxPolyDP(contour, approx, epsilon, true);
            if (approx.size() == 4 && 23500 < abs(contourArea(approx)) && abs(contourArea(approx)) < 23800) {
                for (int i = 0; i < 4; ++i) {
                    circle(img, approx[i], 3, Scalar(255, 0, 0), 3);
                }
                for (int i = 0; i < 4; ++i) {
                    line(img, approx[i], approx[(i + 1) % 4], Scalar(0, 0, 255), 2);
                }
                imwrite("C:\test/rectangle.jpg", img);
                rec_detected = "rectangle";
                break;
            }
        }
        vector<cv::Vec3f> circles;
        cv::HoughCircles(edge_img, circles, cv::HOUGH_GRADIENT, 1, 100, 200, 25, 80, 98);

        if (!circles.empty()) {
            // 반지름들을 저장할 벡터를 생성합니다.
            vector<float> radii;
            // 각 원의 반지름을 radii 벡터에 저장합니다.
            for (const auto& circle : circles) {
                radii.push_back(circle[2]);
            }
            // radii 벡터에 저장된 반지름 중에서 최솟값을 찾습니다.
            sort(radii.begin(), radii.end());
            // 최솟값 출력
            cout << "5개의 최솟 반지름: ";
            for (int i = 0; i < min(5, static_cast<int>(radii.size())); ++i) {
                cout << radii[i] << " ";
            }
            cout << endl;

            // 최솟 반지름을 원으로 그리기
            float min_radius = radii[0];
            for (const auto& circle : circles) {
                cv::Point center(static_cast<int>(circle[0]), static_cast<int>(circle[1]));
                int radius = static_cast<int>(circle[2]); // 반지름을 정수형으로 변환합니다.
                if (radius == static_cast<int>(min_radius)) {
                    cv::circle(img, center, radius, cv::Scalar(0, 255, 0), 3);
                   /* double area = M_PI * pow(radius, 2);
                cout << area << endl;*/
                    imwrite("C:\test/circle.jpg", img);
                if (15000 < radius && radius < 18000) {                  
                    rec_detected = "circle";
                    break;
                }
                }
            }
        }
        cout << rec_detected << endl;
        map<string, string> shape_result;
        if (rec_detected == "rectangle") {
            shape_result["Shape"] = "Success";
        } else if (rec_detected == "circle") {
            shape_result["Shape"] = "Error";
        } else {
            shape_result["Shape"] = "Failed";
        }
        return shape_result;
    }
};

int main() {
    QRcode qr;
    Shapes shape;
    VideoCapture cap(0);
    cap.set(CAP_PROP_FRAME_WIDTH, 460);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);
    cap.set(CAP_PROP_FPS,10);
    while (true) {
        Mat frame;
        bool ret = cap.read(frame);
        if (!ret) {
            cout << "Capture error" << endl;
            continue;
        }
        auto QR = qr.qr_decode(frame);
        int count = 0;
        map<string, string> shape_result;
        for (count = 0; count < 1; ++count) {
            cout << "count: " << count << endl;
            shape_result = shape.shapes_decode(frame);
            if (shape_result["Shape"] != "Failed") {
                break;
            }
            this_thread::sleep_for(chrono::milliseconds(500));
        }
        cout << shape_result["Shape"] << endl;
        if (!QR.empty() && !shape_result.empty()) {
            map<string, string> combined_result = QR;
            combined_result.insert(shape_result.begin(), shape_result.end());
            cout << combined_result["Shape"] << endl;
            break;
        } else if (shape_result["Shape"] == "Error") {
            QR = {{"QR", ""}};
            map<string, string> combined_result = QR;
            combined_result.insert(shape_result.begin(), shape_result.end());
            cout << combined_result["Shape"] << endl;
            break;
        }
        imshow("cam", frame);
        imwrite("/home/nsf/사진/img.jpg", frame);
        imshow("cam", frame);
        if (waitKey(30) >= 0) break;
    }
    return 0;
}

