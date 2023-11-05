"""
    Cver Test - Unit
    Shared - Utils Xlate
    Tests File: cver/src/cver/shared/utils/misc.py

"""
from cver.shared.utils import misc


class TestSharedUtilMisc:

    def test__container_url(self):
        """Test that we can convert a container url to it's usable parts.
        :method: misc.container_url()
        """
        # Test with registry in url
        img_url = "docker.io/calico/node:v3.20.2"
        test_res = misc.container_url(img_url)
        assert isinstance(test_res, dict)
        assert test_res["registry"] == "docker.io"
        assert test_res["image"] == "calico/node"
        assert test_res["tag"] == "v3.20.2"
        assert test_res["full"] == img_url

        # Test without registry
        img_url = "pignus/api:v3.20.2"
        test_res = misc.container_url(img_url)
        assert test_res["registry"] == "docker.io"
        assert test_res["image"] == "pignus/api"
        assert test_res["tag"] == "v3.20.2"
        assert test_res["full"] == "docker.io/%s" % img_url

        # Test minimal
        img_url = "nginx"
        test_res = misc.container_url("nginx")
        assert isinstance(test_res, dict)
        assert test_res["registry"] == "docker.io"
        assert test_res["image"] == "nginx"

        # Test tag with sha
        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller:v1.8.1@sha256:%s" % img_sha
        test_res = misc.container_url(image_url)
        assert isinstance(test_res, dict)
        assert test_res["registry"] == "registry.k8s.io"
        assert test_res["image"] == "ingress-nginx/controller"
        assert test_res["tag"] == "v1.8.1"
        assert test_res["sha"] == img_sha

        # Test only with sha
        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller@sha256:%s" % img_sha
        test_res = misc.container_url(image_url)
        assert isinstance(test_res, dict)
        assert test_res["registry"] == "registry.k8s.io"
        assert test_res["image"] == "ingress-nginx/controller"
        assert test_res["tag"] == "latest"
        assert test_res["sha"] == img_sha

        image_url = "registry.k8s.io/kube-scheduler:v1.24.15"
        test_res = misc.container_url(image_url)
        assert "registry.k8s.io" == test_res["registry"]
        assert "kube-scheduler" == test_res["image"]
        assert "v1.24.15" == test_res["tag"]
        assert "" == test_res["sha"]

    def test__is_fqdn(self):
        """Test that can determin FQDNs
        :method: misc.is_fqdn()
        """
        assert misc.is_fqdn("google.com")
        assert not misc.is_fqdn("google.com/")

    def test__percentize(self):
        """
        :method: misc.percentize()
        """
        assert 50.0 == misc.percentize(2, 4)
        assert 50 == misc.percentize(2, 4, round_int=0)

    def test__strip_trailing_slash(self):
        """Test that we strip trailing slashes.
        :method: misc.strip_trailing_slash()
        """
        assert "google.com" == misc.strip_trailing_slash("google.com")
        assert "google.com" == misc.strip_trailing_slash("google.com/")
        assert "http://localhost" == misc.strip_trailing_slash("http://localhost/")

    def test__add_trailing_slash(self):
        """Test that we add trailing slashes.
        :method: misc.add_trailing_slash()
        """
        assert "google.com/" == misc.add_trailing_slash("google.com")
        assert "google.com/" == misc.add_trailing_slash("google.com/")
        assert "http://localhost/" == misc.add_trailing_slash("http://localhost/")

    def test___get_registry(self):
        """Test that we get a registry domain from a docker image url string.
        :method: misc.registry()
        """
        registry = misc._get_registry("registry.k8s.io/kube-scheduler:v1.24.15")
        assert "registry.k8s.io" == registry

        registry = misc._get_registry("docker.io/calico/node:v3.20.2")
        assert isinstance(registry, str)
        assert registry == "docker.io"

        registry = misc._get_registry("docker.io/calico/node")
        assert isinstance(registry, str)
        assert registry == "docker.io"

        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller:v1.8.1@sha256:%s" % img_sha
        registry = misc._get_registry(image_url)
        assert isinstance(registry, str)
        assert registry == "registry.k8s.io"

    def test___get_image(self):
        """Test that we get a image from a docker url string.
        :method: misc._get_image()
        """
        image_name = misc._get_image("docker.io/calico/node:v3.20.2", "docker.io")
        assert isinstance(image_name, str)
        assert image_name == "calico/node"

        image_name = misc._get_image("docker.io/calico/node", "docker.io")
        assert isinstance(image_name, str)
        assert image_name == "calico/node"

        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller:v1.8.1@sha256:%s" % img_sha
        image_name = misc._get_image(image_url, "registry.k8s.io")
        assert isinstance(image_name, str)
        assert image_name == "ingress-nginx/controller"

        image_name = misc._get_image("nginx")
        assert isinstance(image_name, str)
        assert image_name == "nginx"

    def test___get_tag(self):
        """Test that we get a tag
        :method: misc._get_tag()
        """
        tag = misc._get_tag("docker.io/calico/node:v3.20.2")
        assert isinstance(tag, str)
        assert tag == "v3.20.2"

        tag = misc._get_tag("docker.io/calico/node")
        assert isinstance(tag, str)
        assert "latest" == misc._get_tag("docker.io/calico/node")

        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller:v1.8.1@sha256:%s" % img_sha
        tag = misc._get_tag(image_url)
        assert isinstance(tag, str)
        assert tag == "v1.8.1"

    def test___get_sha(self):
        """Test that we get an image sha
        :method: misc.get_sha()
        """
        sha = misc._get_sha("docker.io/calico/node:v3.20.2")
        assert isinstance(sha, str)
        assert sha == ""

        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller:v1.8.1@sha256:%s" % img_sha
        sha = misc._get_sha(image_url)
        assert isinstance(sha, str)
        assert sha == "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"

        img_sha = "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"
        image_url = "registry.k8s.io/ingress-nginx/controller@sha256:%s" % img_sha
        sha = misc._get_sha(image_url)
        assert isinstance(sha, str)
        assert sha == "e5c4824e7375fcf2a393e1c03c293b69759af37a9ca6abdb91b13d78a93da8bd"

    def test__get_full(self):
        """Test that we can convert a container url to it's usable parts.
        :method: misc.container_url()
        """
        # Test with registry
        img_url = "docker.io/calico/node:v3.20.2"
        the_url_dict = misc.container_url(img_url)
        test_res = misc._get_full(the_url_dict)
        assert test_res == img_url


# End File: cver/tests/unit/shared/utils/test_misc.py
