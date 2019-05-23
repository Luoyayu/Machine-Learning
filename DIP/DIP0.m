img = imread('moe1.jpg');
img_gray = rgb2gray(img);
img_gray=im2double(img_gray)*0.5;

% img = 255 - img;
[M, N] = size(img_gray);
% histogram(img);

% subplot(221);
% imshow(img)
% subplot(224);
% imshow(img_gray)

mu = mean(img_gray(:)); %  列向量

% shape = size(img_gray(:));

% [h, xc] = hist(img_gray(:));
% p = h/sum(h);
% p2 = h/numel(img_gray);
img_eq = histeq(img_gray, 256);
% bar(xc, p2)
imshow(img_gray)
figure, imshow(img_eq)



