
clear;
close all hidden;

% Get images

orgS1 = imread("Seattle 1.jpg");
orgS2 = imread("Seattle 2.jpg");

binS1 = imbinarize(orgS1);
binS2 = imbinarize(orgS2);

histOrg1 = imhist(orgS1);
histOrg2 = imhist(orgS2);
histBin1 = imhist(binS1);
histBin2 = imhist(binS2);

% Display these as images

figure;
subplot(2,4,1); imshow(orgS1); title("Seattle 1");
subplot(2,4,2); imshow(binS1); title("Bin Seattle 1");
subplot(2,4,3); imshow(orgS2); title("Seattle 2");
subplot(2,4,4); imshow(binS2); title("Bin Seattle 2");
subplot(2,4,5); bar(histOrg1); title("Seattle 1 Hist");
subplot(2,4,6); bar(histBin1); title("Bin Seattle 1 Hist");
subplot(2,4,7); bar(histOrg2); title("Seattle 2 Hist");
subplot(2,4,8); bar(histBin2); title("Bin Seattle 2 Hist");

% Local thresholding method for first image

s1Thresh = localThreshold(orgS1,540,1900,30,0.7);

% Some post processing 

SE = strel("square",2);

s1Processed = imopen(s1Thresh,SE);
s1Processed = bwmorph(s1Processed,"thin",1);

figure;
subplot(1,2,1); imshow(s1Thresh); title("Seattle 1");
subplot(1,2,2); imshow(s1Processed); title("Processed");

% Local thresholding for second image

s2Thresh = localThreshold(orgS2,800,1550,15,0.8);

% Some post processing

s2Processed = imopen(s2Thresh,SE);
s2Processed = bwmorph(s2Processed,"thin",1);

figure;
subplot(1,2,1); imshow(s2Thresh); title("Seattle 2");
subplot(1,2,2); imshow(s2Processed); title("Processed");

return;



function output = localThreshold(processImage, imageTop, imageBot, windowSize, thresholdFactor)

    output = double(processImage);  % Work with double for precision

    % Precompute the integral image
    integralImg = cumsum(cumsum(output, 2), 1);

    [maxR, maxC] = size(output);

    % Clear the specified region once at the start
    if imageTop > 0 && imageBot > 0
        output(imageTop:imageBot, :) = 1;
    end

    % Main loop with window traversal
    for topR = 1:windowSize:maxR
        botR = min(topR + windowSize - 1, maxR);

        for topC = 1:windowSize:maxC
            botC = min(topC + windowSize - 1, maxC);

            % Calculate local mean using the integral image
            totalPixels = (botR - topR + 1) * (botC - topC + 1);
            localSum = getWindowSum(integralImg, topR, botR, topC, botC);
            localMean = localSum / totalPixels;
            T = localMean * thresholdFactor;

            % Threshold the window (vectorized operation)
            window = output(topR:botR, topC:botC);
            window(window < T) = 0;
            window(window >= T) = 1;
            output(topR:botR, topC:botC) = window;

        end
    end

    output = logical(output);  % Convert to logical once at the end
end

% Helper function to get window sum from integral image
function s = getWindowSum(integralImg, topR, botR, topC, botC)
    s = integralImg(botR, botC) ...
        - (topR > 1) * integralImg(topR, botC) ...
        - (topC > 1) * integralImg(botR, topC) ...
        + (topR > 1 && topC > 1) * integralImg(topR, topC);
end


