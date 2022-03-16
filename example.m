colormapnames=colormap_matplotlib('list');
colormapnames=colormapnames(cellfun(@(x)~endsWith(x,'_r'),colormapnames));
figure('color',[1 1 1],'defaulttextinterpreter','none');
set(gcf,'position',get(0,'screensize'));

for c = 1:numel(colormapnames)
    subplot(ceil(sqrt(numel(colormapnames))),ceil(sqrt(numel(colormapnames))),c);
    imagesc(linspace(0,1,256));
    colormap(gca,colormap_matplotlib(colormapnames{c}));
    title(colormapnames{c});
    set(gca,'xtick',[],'ytick',[]);
    box on;
    fprintf('%s\n',colormapnames{c});
end
